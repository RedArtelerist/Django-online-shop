# Generated by Django 3.1.1 on 2020-09-25 19:37

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20200925_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='placeholder.png', null=True, upload_to=main.models.upload_path),
        ),
    ]
