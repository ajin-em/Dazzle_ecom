# Generated by Django 4.2.7 on 2023-11-30 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0052_remove_cart_final_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
