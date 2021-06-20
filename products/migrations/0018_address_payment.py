# Generated by Django 3.2 on 2021-06-07 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20210607_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('locality', models.CharField(max_length=50)),
                ('addr', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('AP', 'Andhra Pradesh'), ('KA', 'Karnataka'), ('TN', 'Tamil Nadu')], max_length=20, null=True)),
                ('aphone', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_option', models.CharField(max_length=50)),
            ],
        ),
    ]
