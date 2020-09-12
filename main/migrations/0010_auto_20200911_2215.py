# Generated by Django 3.1.1 on 2020-09-11 19:15

from django.db import migrations, models
import main.validations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200911_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[main.validations.validate_price], verbose_name='Price'),
        ),
    ]
