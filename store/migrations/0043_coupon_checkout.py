# Generated by Django 4.2.7 on 2023-11-17 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0042_alter_product_variant_actual_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coupon', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkout', to='store.cartitem')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkout', to='store.coupon')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product_variant')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='checkout', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
