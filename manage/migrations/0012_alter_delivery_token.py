# Generated by Django 4.0.2 on 2022-02-15 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0011_product_is_special_alter_delivery_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='token',
            field=models.CharField(default='3UN9QI', max_length=6),
        ),
    ]
