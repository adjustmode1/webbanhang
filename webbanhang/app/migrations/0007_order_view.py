# Generated by Django 4.2.1 on 2023-06-10 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_product_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='view',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
