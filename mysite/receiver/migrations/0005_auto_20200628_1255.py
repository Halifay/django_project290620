# Generated by Django 3.0 on 2020-06-28 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receiver', '0004_auto_20200628_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
