# Generated by Django 4.2.7 on 2023-11-20 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_useraddress_landmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='landmark',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='pincode',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
