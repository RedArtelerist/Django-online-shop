from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_discount(value):
    if value > 100:
        raise ValidationError(
            _('%(value)s is not correct discount'),
            params={'value': value},
        )


def validate_price(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not correct price'),
            params={'value': value},
        )


def validate_product_year(value):
    if value < 2005 or value > datetime.datetime.now().year:
        raise ValidationError(
            _('%(value)s is not correct year'),
            params={'value': value},
        )
