# Generated by Django 4.2.7 on 2023-11-10 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_rename_image_productimage_extra_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_variant',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='variant_main_images'),
        ),
    ]
