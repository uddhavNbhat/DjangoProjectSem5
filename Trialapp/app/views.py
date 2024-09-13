from django.shortcuts import render,redirect
from .forms import Signup
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from .models import Profile,Product,SellingUser,Cart
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from uuid import uuid4


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

@login_required
def register_seller(request):
    selling_user = SellingUser.objects.get(id = request.user.id)
    if selling_user.is_seller:
        return redirect("/sellProduct/1/")
    if request.method == 'POST':
        company_name = request.POST['EnterpriseName']
        seller_type = request.POST['SellerType']
        selling_user.company_name = company_name
        selling_user.seller_type = seller_type
        selling_user.is_seller = True
        if selling_user.seller_uid is None:
            selling_user.seller_uid = uuid4()
        selling_user.save()
        return redirect("/sellProduct/1/")

    return render(request, "seller.html")

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = SellingUser.objects.get(id = request.user.id)
        user.delete()
        return redirect('/login/')
    else:
        return redirect('/profile/')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/login/')

@login_required
def sell_product(request, page=1):
    selling_user = SellingUser.objects.get(id = request.user.id)
    if not selling_user.seller_uid:
        return redirect('/sellerReg/')
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

@login_required
def delete_product(request , prod_id):
    if request.method == 'POST':
        product = Product.objects.get(id = prod_id)
        profile = Profile.objects.get(user_profile = request.user.id)
        profile.prod_listed = profile.prod_listed - 1
        profile.save()
        product.delete()
        return redirect("/sellProduct/1/")

@login_required
def checkout_product(request , prod_id):
    product = Product.objects.get(id = prod_id)
    seller = SellingUser.objects.get(id = request.user.id)
    if request.method == 'POST':
        if(product.id):
            product_price = product.price
            cart = Cart(
                quantity = 1,
                price = product_price,
            )
            cart.save()
        return render(request, 'checkout.html')

    context = {
                'product_name' : product.name,
                'product_condition' : product.conditon,
                'product_type' : product.type,
                'product_detail' : product.detail,
                'product_price' : product.price,
                'product_image' : product.image,
                'product_seller' : seller.company_name,
            }

    return render(request,'checkout.html',context)
