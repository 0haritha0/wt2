# Generated by Django 3.2 on 2021-06-09 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_alter_address_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=10),
        ),
    ]
