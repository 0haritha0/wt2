# Generated by Django 3.2 on 2021-06-07 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_alter_address_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='paymode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.payment'),
        ),
    ]