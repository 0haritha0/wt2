# Generated by Django 3.2 on 2021-06-07 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20210607_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='pincode',
            field=models.CharField(max_length=6, null=True),
        ),
    ]