# Generated by Django 5.0.4 on 2024-07-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_bill_menu_menuitem_order_item_productitem_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stockmanagement",
            name="now_available",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="stockmanagement",
            name="product_deduce",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]