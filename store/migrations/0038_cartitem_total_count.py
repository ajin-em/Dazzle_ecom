# Generated by Django 4.2.7 on 2023-11-17 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_alter_cart_final_price_alter_cart_total_actual_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
