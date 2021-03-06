# Generated by Django 3.2 on 2021-06-07 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20210607_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paymode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.payment'),
        ),
    ]
