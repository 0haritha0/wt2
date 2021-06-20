# Generated by Django 3.2 on 2021-06-09 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_auto_20210609_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.cart'),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='paymode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.payment'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=10),
        ),
    ]
