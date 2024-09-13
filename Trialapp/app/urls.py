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
    path('deleteProfile/',views.delete_user, name='delete_user'),
    path('sellProduct/<int:page>/', views.sell_product, name="sellProduct"),
    path('deleteProduct/<int:prod_id>/',views.delete_product, name="deleteProduct"),
    path('sellerReg/',views.register_seller, name="createSeller"),
    path('checkout/<int:prod_id>/',views.checkout_product, name="buy"),
]
