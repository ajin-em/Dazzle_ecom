# Generated by Django 4.2.7 on 2023-11-07 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='actual_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
