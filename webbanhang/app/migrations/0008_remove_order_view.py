# Generated by Django 4.2.1 on 2023-06-10 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_order_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='view',
        ),
    ]
