# Generated by Django 4.0.2 on 2022-02-14 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='profile_pic',
            new_name='image',
        ),
    ]
