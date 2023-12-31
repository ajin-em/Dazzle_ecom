# Generated by Django 4.2.7 on 2023-11-17 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_remove_productimage_is_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_actual_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='total_selling_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
