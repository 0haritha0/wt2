# Generated by Django 3.2 on 2021-06-10 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0039_alter_tips_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tips',
            name='status',
            field=models.CharField(choices=[('U', 'Unpublish'), ('P', 'Publish')], default='Unpublish', max_length=20, null=True),
        ),
    ]
