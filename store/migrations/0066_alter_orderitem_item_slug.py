# Generated by Django 4.2.7 on 2023-12-18 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0065_orderitem_item_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item_slug',
            field=models.SlugField(max_length=200, null=True),
        ),
    ]
