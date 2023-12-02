# Generated by Django 4.2.7 on 2023-11-17 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0045_alter_checkout_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='coupon',
        ),
        migrations.AddField(
            model_name='checkout',
            name='payment_method',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='coupon',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coupon',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
