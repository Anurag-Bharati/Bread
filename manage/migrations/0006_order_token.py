# Generated by Django 4.0.2 on 2022-02-15 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0005_alter_product_is_featured_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='token',
            field=models.CharField(default='HJ2kAN', max_length=6),
        ),
    ]
