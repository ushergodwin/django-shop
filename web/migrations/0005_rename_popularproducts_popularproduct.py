# Generated by Django 4.0.5 on 2022-08-06 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_popularproducts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PopularProducts',
            new_name='PopularProduct',
        ),
    ]