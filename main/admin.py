from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label="Description", widget=CKEditorUploadingWidget())
    specifications = forms.CharField(label="Specifications", widget=CKEditorUploadingWidget())

    class Meta:
        description = Product
        fields = '__all__'

# Register your models here.


admin.site.register(Category)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'email')
    readonly_fields = ('name', 'user', 'email')


class ImagesInline(admin.TabularInline):
    model = ImageItem
    extra = 1
    classes = ('collapse',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" style="max-height: 250px"')

    get_image.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'company', 'isActive', 'digital', 'get_image')
    readonly_fields = ('get_image',)
    list_filter = ('category', 'company', 'year')
    search_fields = ('name', 'category__name', 'company__name')
    inlines = [ImagesInline]
    save_on_top = True
    list_editable = ('isActive',)
    form = ProductAdminForm
    fieldsets = (
        (None, {
            "fields": (('image', 'get_image', ), )
        }),
        (None, {
            "fields": ('name', 'description', 'shortSpecifications', 'specifications',)
        }),
        (None, {
            "fields": (('price', 'discount', 'year'),)
        }),
        (None, {
            "fields": ('digital', 'isActive')
        }),
        (None, {
            "fields": (('category', 'company'),)
        }),
    )

    def get_image(self, obj):
        if obj.image.url:
            pass
        else:
            return mark_safe(f'<img src= width="100" style="max-height: 250px"')
        return mark_safe(f'<img src={obj.image.url} width="100" style="max-height: 250px"')

    get_image.short_description = 'Image'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_id', 'data_order', 'customer', 'get_total_price', 'complete')
    list_display_links = ('transaction_id', )
    readonly_fields = ('customer', 'transaction_id', 'data_order', )

    def get_total_price(self, obj):
        return f"{obj.get_cart_total:.{2}f}"

    get_total_price.short_description = 'Total price'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'data_added', 'get_total_price', 'get_image')
    readonly_fields = ('product', 'order',)
    fields = ('product', 'order', 'quantity')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.product.image.url} width="100" style="max-height: 250px"')

    def get_total_price(self, obj):
        return f"{obj.get_total:.{2}f}"

    get_image.short_description = 'Image'
    get_total_price.short_description = 'Total price'


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'data_added', 'country', 'state', 'city', 'address')
    readonly_fields = ('customer', 'order', )

    fieldsets = (
        (None, {
            "fields": ('order', 'customer',)
        }),
        (None, {
            "fields": (('country', 'state',),)
        }),
        (None, {
            "fields": (('city', 'address'),)
        }),
        (None, {
            "fields": ('zipcode',)
        }),
    )


@admin.register(ImageItem)
class ImageItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'get_image',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" style="max-height: 250px""')

    get_image.short_description = 'Image'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user', 'product', 'parent', 'data_added')
    readonly_fields = ('user', 'parent', 'data_added', 'name', 'email')

    fieldsets = (
            (None, {
                "fields": (('user', 'product', 'data_added'),)
            }),
            (None, {
                "fields": (('name', 'email',),)
            }),
            (None, {
                "fields": ('parent', 'text',)
            }),
        )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'product', 'data_added', 'status')
    list_filter = ['status']
    readonly_fields = ('subject', 'text', 'user', 'product', 'rate', 'data_added')

    fieldsets = (
            (None, {
                "fields": ('status',)
            }),
            (None, {
                "fields": (('user', 'product', 'data_added'),)
            }),
            (None, {
                "fields": ('subject', 'text', 'rate')
            }),
        )


