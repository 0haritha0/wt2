# Generated by Django 3.2 on 2021-06-10 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_tips'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tips',
            name='status',
            field=models.CharField(choices=[('P', 'Publish'), ('U', 'Unpublish')], max_length=20, null=True),
        ),
    ]
