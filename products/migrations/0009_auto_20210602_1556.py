# Generated by Django 3.2 on 2021-06-02 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_product_fprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_discount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_fprice',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.FloatField(),
        ),
    ]
