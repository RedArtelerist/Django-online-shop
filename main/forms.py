from django import forms
from .models import *


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)
        labels = {
            'name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'country')
        labels = {
            'name': 'Name',
            'country': 'Country'
        }

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'digital', 'image', 'description', 'specifications', 'discount', 'year', 'isActive',
                  'category', 'company']
        labels = {
            'name': 'Product Name',
            'price': 'Price',
            'digital': 'Digital',
            'image': 'Load image',
            'description': 'Description',
            'specifications': 'Specification',
            'discount': 'Discount',
            'year': 'Year',
            'isActive': 'Active',
            'category': 'Category',
            'company': 'Company'
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['category'].empty_label="Select"
        self.fields['company'].empty_label="Select"