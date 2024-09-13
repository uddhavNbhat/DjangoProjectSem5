# Generated by Django 5.1 on 2024-08-30 19:16

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('conditon', models.CharField(choices=[('New', 'New'), ('Used', 'Used'), ('Refurbished', 'Refurbished')], default='New', max_length=100)),
                ('type', models.CharField(choices=[('Electronics', 'Electronics'), ('Clothing', 'Clothing'), ('Footwear', 'Footwear'), ('Home Accessory', 'Home Accessory'), ('Vehicle Accessory', 'Vehicle Accessory'), ('Toys', 'Toys'), ('Sport Equipment', 'Sport Equipment')], max_length=100)),
                ('detail', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='product_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qunatity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('prod', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='SellingUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('seller_type', models.CharField(blank=True, choices=[('Manufacturer', 'Manufacturer'), ('Private', 'Private'), ('Reseller', 'Reseller')], max_length=20, null=True)),
                ('company_name', models.CharField(blank=True, max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='sellinguser_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='sellinguser_permissions_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='app.product')),
                ('user_review', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='app.sellinguser')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('prod_bought', models.IntegerField(default=0)),
                ('prod_sold', models.IntegerField(default=0)),
                ('user_profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.sellinguser')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='selling_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='app.sellinguser'),
        ),
    ]
