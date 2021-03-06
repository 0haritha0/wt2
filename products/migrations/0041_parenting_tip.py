# Generated by Django 3.2 on 2021-06-10 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0040_alter_tips_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='parenting_tip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', '1-6 Months'), ('2', '1 year'), ('3', '1-2 years'), ('4', '2+ years')], max_length=20)),
                ('tip_title', models.CharField(max_length=200)),
                ('tip_desc', models.CharField(max_length=500)),
            ],
        ),
    ]
