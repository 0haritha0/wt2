# Generated by Django 3.2 on 2021-06-10 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0041_parenting_tip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parenting_tip',
            old_name='status',
            new_name='age',
        ),
    ]