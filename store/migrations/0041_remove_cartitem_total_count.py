# Generated by Django 4.2.7 on 2023-11-17 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0040_remove_cartitem_actual_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='total_count',
        ),
    ]
