# Generated by Django 3.1.1 on 2020-09-23 16:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20200923_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=100, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=100, null=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='User name must be Alphanumerical', regex='^[a-zA-Z0-9\\s_-]*$')], verbose_name='Name'),
        ),
    ]