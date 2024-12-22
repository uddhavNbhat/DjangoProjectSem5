from django.shortcuts import render,redirect
from .forms import Signup
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from .models import Profile,Product,SellingUser,Cart
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from uuid import uuid4
from django.http import JsonResponse
import json

#signup view
def signup(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            date = datetime.now()
            new_profile = Profile(
                user_profile = user,
                created_at = date,
                prod_listed = 0,
                prod_bought = 0,
                prod_sold = 0,
            )
            new_profile.save()
            return redirect('/login/')
    else:
        form = Signup()

    return render(request, 'signup.html', {'form': form})

#login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Attempting to authenticate user: {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Authentication successful")
            login(request,user)
            return redirect('/')
        else:
            print("Authentication failed")
            return render(request, 'login.html', {'error' : 'Invalid Credentials'})


    return render(request, 'login.html')

# main page view(index) and applied paginator from django
@login_required
def index(request,page=1):
    username = request.user.username
    products = Product.objects.all()
    paging = Paginator(products,9)
    try:
        products = paging.page(page)
    except PageNotAnInteger:
        products = paging.page(1)
    except EmptyPage:
        products = paging.page(paging.num_pages)

    return render(request, 'index.html', {'username': username, 'products': products,'current_page': page,'total_pages': paging.num_pages})

# user profile view
@login_required
def user_profile(request):
    user = SellingUser.objects.get(id = request.user.id)
    profile = Profile.objects.get(user_profile = user)

    context = {
        'username' : user.username,
        'email' : user.email,
        'created_at' : profile.created_at,
        'prod_listed' : profile.prod_listed,
        'prod_bought' : profile.prod_bought,
        'prod_sold' : profile.prod_sold,
        'company_name' : user.company_name,
        'seller_type' : user.seller_type,
        'is_seller' : user.is_seller,
    }
    return render(request, 'profile.html', context)

#user profile update view using PATCH function through json content
@login_required
@csrf_protect
def update_profile(request):
    if request.method == "PATCH":
        user = SellingUser.objects.get(id=request.user.id)
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            email = data.get('email')
            if username:
                if SellingUser.objects.filter(username=username).exclude(id=user.id).exists():
                    return JsonResponse({"error": "Username already exists"}, status=400)
                user.username = username
            if email:
                user.email = email
            user.save()
            return JsonResponse({"success": "Profile updated successfully"})
        except SellingUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)

# register seller through uuid
@login_required
def register_seller(request):
    selling_user = SellingUser.objects.get(id = request.user.id)
    if selling_user.is_seller:
        return redirect("/product/sell/1/")
    if request.method == 'POST':
        company_name = request.POST['EnterpriseName']
        seller_type = request.POST['SellerType']
        selling_user.company_name = company_name
        selling_user.seller_type = seller_type
        selling_user.is_seller = True
        if selling_user.seller_uid is None:
            selling_user.seller_uid = uuid4()
        selling_user.save()
        return redirect("/product/sell/1/")

    return render(request, "seller.html")

# delete user profile/account
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = SellingUser.objects.get(id = request.user.id)
        user.delete()
        return redirect('/login/')
    else:
        return redirect('/profile/')

#logut
@login_required
def user_logout(request):
    logout(request)
    return redirect('/login/')

#sell a product as a seller, applied pagination from django
@login_required
def sell_product(request, page=1):
    selling_user = SellingUser.objects.get(id = request.user.id)
    if not selling_user.seller_uid:
        return redirect('/seller/register/')
    if request.method == 'POST':
        product_name = request.POST["Productname"]
        product_condition = request.POST["ProductCondition"]
        product_type = request.POST["ProductType"]
        product_detail = request.POST["ProductDetail"]
        product_price = int(request.POST["ProductPrice"])
        product_image = request.FILES.get("ProductImage")
        product_save = Product(name = product_name,
                               conditon = product_condition,
                               type = product_type,
                               detail = product_detail,
                               price = product_price,
                               image = product_image,
                               selling_user = selling_user)
        product_save.save()
        profile = Profile.objects.get(user_profile = request.user.id)
        profile.prod_listed = profile.prod_listed + 1
        profile.save()
        return redirect('sellProduct', page = page)

    all_products = Product.objects.filter(selling_user = selling_user)
    paging = Paginator(all_products,9)
    try:
        products = paging.page(page)
    except PageNotAnInteger:
        products = paging.page(1)
    except EmptyPage:
        products = paging.page(paging.num_pages)
    return render(request, "sell.html", {
        'current_page': page,
        'products': products,
        'total_pages': paging.num_pages,
        'username' : selling_user.company_name,
        'seller': selling_user.is_seller,
    })

# delete product
@login_required
def delete_product(request , prod_id):
    if request.method == 'POST':
        product = Product.objects.get(id = prod_id)
        profile = Profile.objects.get(user_profile = request.user.id)
        profile.prod_listed = profile.prod_listed - 1
        profile.save()
        product.delete()
        return redirect("/product/sell/1/")

# checkout cart functionality
@login_required
def checkout_product(request , prod_id):
    product = Product.objects.get(id = prod_id)
    if request.method == "POST":
        user = SellingUser.objects.get(id = request.user.id)
        cart_item, created = Cart.objects.get_or_create(user = user,prod=product, quantity=1, price=product.price)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('/cart/')

    return render(request,'checkout.html')

# view cart functionality
@login_required
def checkout(request):
    user= SellingUser.objects.get(id=request.user.id)
    cart = Cart.objects.filter(user = user)
    print(cart.values())
    total_price = sum(item.price * item.quantity for item in cart)
    context = {
                'total_price': total_price,
                'cart' : cart,
            }
    return render(request,'checkout.html',context)

# update cart items
@login_required
def update_cart(request):
    if request.method == "POST":
        user = SellingUser.objects.get(id=request.user.id)
        cart = Cart.objects.filter(user = user)
        total_price = 0
        for item in cart:
            quantity = request.POST.get(f'quantity_{item.prod.id}')
            if quantity:
                item.quantity = int(quantity)
                print(item.quantity)
                item.save()
            total_price += item.price * item.quantity
        print(total_price)
        context = {
            'total_price' : total_price,
            'cart' : cart
        }
        return render(request,'checkout.html', context)
    return render(request, 'checkout.html', context)

# remove cart items
@login_required
def remove_cart_item(request,cart_id):
    if request.method == "POST":
        cart = Cart.objects.get(id=cart_id)
        cart.quantity = 0
        cart.delete()
        return redirect('/cart/')
    return render(request,'checkout.html')

#move to payment portal
@login_required
def to_payment(request):
    user = SellingUser.objects.get(id = request.user.id)
    user_cart_products = Cart.objects.filter(user=user).select_related('prod')
    prices = [ x.price for x in user_cart_products]
    names = [ x.prod.name for x in user_cart_products]
    print(prices)
    print(names)
    context = {
        'price' : prices,
        'names' : names
    }
    return render(request, 'payment.html', context)

# view product page
@login_required
def product_page(request,prod_id):
    product = Product.objects.get(id = prod_id)
    return render(request, 'productpage.html', {'product':product})


