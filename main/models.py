from django.core.validators import RegexValidator
from django.db import models
from .validations import *
from django.contrib.auth.models import User
import decimal
import datetime


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Name', max_length=100, null=True, unique=True, validators=[RegexValidator(
        regex='^[a-zA-Z0-9\s_-]*$',
        message='User name must be Alphanumerical',
        code='invalid_username'
    ), ])
    email = models.EmailField('Email', max_length=100, null=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Category(models.Model):
    name = models.CharField('Name', max_length=20, unique=True, validators=[RegexValidator(
        regex='^[a-zA-Z\s_-]*$',
        message='Category must be Alphabetic',
        code='invalid_categoryname'
    ), ])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Company(models.Model):
    name = models.CharField('Name', max_length=20, unique=True, validators=[RegexValidator(
        regex='^[a-zA-Z\s_-]*$',
        message='Company name must be Alphabetic',
        code='invalid_companytname'
    ), ])
    country = models.CharField('Country', max_length=15, validators=[RegexValidator(
        regex='^[a-zA-Z\s_-]*$',
        message='Country must be Alphabetic',
        code='invalid_countryname'
    ), ])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Product(models.Model):
    image = models.ImageField(null=True, blank=True, default='placeholder.png')
    name = models.CharField('Name', max_length=50, null=True, unique=True, validators=[RegexValidator(
        regex='^[a-zA-Z0-9/\s)(._-]*$',
        message='Product name must be Alphabetic',
        code='invalid_productname'
    ), ])
    description = models.TextField('Description', max_length=3000, blank=True, null=True)
    shortSpecifications = models.TextField('Short specifications', max_length=500, null=True)
    specifications = models.TextField('Specifications', max_length=3000, null=True)
    price = models.DecimalField('Price', default=0, max_digits=10, decimal_places=2, validators=[validate_price])
    discount = models.PositiveSmallIntegerField('Discount', default=0, null=True, validators=[validate_discount])
    year = models.PositiveSmallIntegerField('Year', default=datetime.datetime.now().year,
                                            validators=[validate_product_year])
    digital = models.BooleanField(default=False, null=True, blank=False)
    isActive = models.BooleanField(default=True)
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def discount_price(self):
        return self.price * decimal.Decimal(1 - self.discount / 100)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'media/placeholder.png'
        return url

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ImageItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, default='placeholder.png')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'media/placeholder.png'
        return url

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Product Gallery'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    data_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def shipping(self):
        shipping = False;
        orderItems = self.orderitem_set.all()

        for item in orderItems:
            if not item.product.digital:
                shipping = True
        return shipping

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.discount_price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField('Country', max_length=30, null=True, validators=[RegexValidator(
        regex='^[a-zA-Z\s_-]*$',
        message='Country must be Alphabetic',
        code='invalid_countryname'
    ), ])
    city = models.CharField('City', max_length=30, null=True, validators=[RegexValidator(
        regex='^[a-zA-Z\s_-]*$',
        message='City must be Alphabetic',
        code='invalid_cityname'
    ), ])
    state = models.CharField('State', max_length=30, null=True, validators=[RegexValidator(
        regex='^[a-zA-Z\s_-]*$',
        message='State must be Alphabetic',
        code='invalid_statename'
    ), ])
    address = models.CharField('Address', max_length=200, null=True, validators=[RegexValidator(
        regex='^[a-zA-Z0-9/\\s_-]*$',
        message='Address must be Alphanumerical',
        code='invalid_addressname'
    ), ])
    zipcode = models.CharField('Zipcode', max_length=10, null=True, validators=[RegexValidator(
        regex='(^\d{5}$)|(^\d{5}-\d{4}$)',
        message='Zipcode must contains 5 digits',
        code='invalid_zipcodename'
    ), ])
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Shipping address'
        verbose_name_plural = 'Shipping addresses'
