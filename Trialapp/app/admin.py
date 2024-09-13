from django.contrib import admin
from .models import Product,Profile,SellingUser,Cart,Review
# Register your models here.

admin.site.register(SellingUser)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Review)