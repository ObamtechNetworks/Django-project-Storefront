# Generated by Django 5.1.5 on 2025-02-09 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_price_in_product_to_unit_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='-'),
            preserve_default=False,
        ),
    ]
