from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils import timezone
import uuid
# Create your models here.

class SellingUser(AbstractUser):
    DIRECT_TO_CONSUMER = "Manufacturer"
    PRIVATE = "Private"
    RESELLER = "Reseller"
    TYPES_OF_SELLER = [
        (DIRECT_TO_CONSUMER,"Manufacturer"),
        (PRIVATE ,"Private"),
        (RESELLER,"Reseller")
    ]
    seller_uid = models.UUIDField(editable=False, unique=True, null=True, blank=True, default=None)
    seller_type = models.CharField(max_length=20,null=True,choices=TYPES_OF_SELLER,blank=True, default=None)
    company_name = models.CharField(max_length=50,null=True,blank=True,default=None)
    is_seller = models.BooleanField(default=False)


    groups = models.ManyToManyField(
        Group,
        related_name='sellinguser_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='sellinguser_permissions_set',
        blank=True
    )


class Product(models.Model):
    NEW = 'New'
    USED = 'Used'
    REFURBISHED = 'Refurbished'
    CONDITION_CHOICES = [
        (NEW, 'New'),
        (USED, 'Used'),
        (REFURBISHED, 'Refurbished')
    ]
    ELECTRONICS = 'Electronics'
    CLOTHING = 'Clothing'
    FOOTWEAR = 'Footwear'
    HOMEACCESSORY = 'Home Accessory'
    VEHICLEACCESSORY = 'Vehicle Accessory'
    TOYS = 'Toys'
    SPORTEQUIPMENT = 'Sport Equipment'
    TYPES_OF_PRODUCTS = [
        (ELECTRONICS,'Electronics'),
        (CLOTHING,'Clothing'),
        (FOOTWEAR,'Footwear'),
        (HOMEACCESSORY,'Home Accessory'),
        (VEHICLEACCESSORY,'Vehicle Accessory'),
        (TOYS,'Toys'),
        (SPORTEQUIPMENT,'Sport Equipment')
    ]
    selling_user = models.ForeignKey(SellingUser, on_delete=models.PROTECT, default=None)
    name = models.CharField(max_length=100,null=False)
    conditon = models.CharField(max_length=100,default="New",choices=CONDITION_CHOICES)
    type = models.CharField(max_length=100,null=False, choices=TYPES_OF_PRODUCTS)
    detail = models.TextField(null=False)
    price = models.DecimalField(null=False,max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=False)

class Profile(models.Model):
    user_profile = models.OneToOneField(SellingUser, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=timezone.now, null=False)
    prod_listed = models.PositiveIntegerField(default=0)
    prod_bought = models.PositiveIntegerField(default=0)
    prod_sold = models.PositiveIntegerField(default=0)

class Cart(models.Model):
    user = models.ForeignKey(SellingUser, on_delete=models.PROTECT, default=None)
    prod = models.ForeignKey(Product, on_delete=models.PROTECT, default=None)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

class Review(models.Model):
    user_review = models.ForeignKey(SellingUser, on_delete=models.PROTECT, default=None)
    product = models.ForeignKey(Product,default=None,on_delete=models.PROTECT)
    rating = models.PositiveIntegerField(null=False)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, null=False)






