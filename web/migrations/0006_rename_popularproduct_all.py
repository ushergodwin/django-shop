# Generated by Django 4.0.5 on 2022-08-06 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_rename_popularproducts_popularproduct'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PopularProduct',
            new_name='All',
        ),
    ]
