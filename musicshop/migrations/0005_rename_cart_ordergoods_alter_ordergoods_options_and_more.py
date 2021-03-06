# Generated by Django 4.0.4 on 2022-04-24 15:56

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('musicshop', '0004_alter_catalog_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart',
            new_name='OrderGoods',
        ),
        migrations.AlterModelOptions(
            name='ordergoods',
            options={'verbose_name': 'Заказ/Товары', 'verbose_name_plural': 'Заказы/Товары'},
        ),
        migrations.AlterField(
            model_name='catalog',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['vendor_code'], verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', verbose_name='URL'),
        ),
    ]
