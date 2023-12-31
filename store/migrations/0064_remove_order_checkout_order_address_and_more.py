# Generated by Django 4.2.7 on 2023-12-09 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_useraddress_mobile'),
        ('store', '0063_order_coupon_price_order_final_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='checkout',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.useraddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Checkout',
        ),
    ]
