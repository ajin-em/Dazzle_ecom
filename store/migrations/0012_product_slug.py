from django.db import migrations, models
from django.utils.text import slugify

# def populate_slugs(apps, schema_editor):
#     print('populate_slugs function executed')  # Add this line
#     Product = apps.get_model('store', 'product')
#     for instance in Product.objects.all():
#         if not instance.slug and instance.title:
#             instance.slug = slugify(instance.title)
#             instance.save()

class Migration(migrations.Migration):
    print('Migration class executed')  # Add this line
    dependencies = [
        ('store', '0011_productimage_is_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
    ]
