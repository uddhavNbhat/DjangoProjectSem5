# Generated by Django 5.1 on 2024-08-31 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_profile_is_seller_sellinguser_is_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellinguser',
            name='seller_uid',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
    ]
