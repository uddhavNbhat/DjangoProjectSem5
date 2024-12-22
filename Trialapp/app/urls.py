from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/1/', permanent=True)),
    path('<int:page>/',views.index, name = 'index'),
    path('signup/',views.signup, name = 'signup'),
    path('login/',views.user_login, name = 'login'),
    path('profile/',views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/delete/',views.delete_user, name='delete_user'),
    path('profile/update/',views.update_profile, name='update_user'),
    path('product/sell/<int:page>/', views.sell_product, name="sellProduct"),
    path('product/delete/<int:prod_id>/',views.delete_product, name="deleteProduct"),
    path('seller/register/',views.register_seller, name="createSeller"),
    path('cart/<int:prod_id>/',views.checkout_product, name="checkout_prod"),
    path('cart/',views.checkout, name="checkout"),
    path('cart/delete/<int:cart_id>/',views.remove_cart_item, name="removeCartItem"),
    path('cart/update/',views.update_cart,name="update_cart"),
    path('payment/',views.to_payment,name='payment'),
    path('product/<int:prod_id>/',views.product_page, name="product_page"),
]
