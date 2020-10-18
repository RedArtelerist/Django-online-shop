# Generated by Django 3.1.1 on 2020-09-23 15:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='customer',
        ),
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=100, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=100, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='User name must be Alphanumerical', regex='^[a-zA-Z0-9\\s_-]*$')], verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]