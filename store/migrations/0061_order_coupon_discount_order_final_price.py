# Generated by Django 4.2.7 on 2023-12-09 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0060_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='final_price',
            field=models.IntegerField(default=0),
        ),
    ]
