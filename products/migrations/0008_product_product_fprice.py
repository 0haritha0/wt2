# Generated by Django 3.2 on 2021-06-02 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210602_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_fprice',
            field=models.IntegerField(default=0),
        ),
    ]