# Generated by Django 4.0.2 on 2022-02-11 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.TextField(null=True),
        ),
    ]
