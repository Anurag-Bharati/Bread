# Generated by Django 4.0.2 on 2022-02-15 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0010_alter_delivery_token_specialproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_special',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='token',
            field=models.CharField(default='ZDBPF7', max_length=6),
        ),
        migrations.DeleteModel(
            name='SpecialProduct',
        ),
    ]
