from django.urls import path, include
from django.conf.urls import url
from . import views
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [

    path('', views.index, name='home'),
    path('store', views.store, name='store'),
    path('about', views.about, name='about'),
    url(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

    path('category/', views.category_form, name='category_insert'),  # get and post req. for insert operation
    path('category/<int:id>/', views.category_form, name='category_update'),  # get and post req. for update operation
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/list/', views.category_list, name='category_list'), # get req. to retrieve and display all records

    path('company/', views.company_form, name='company_insert'),  # get and post req. for insert operation
    path('company/<int:id>/', views.company_form, name='company_update'),  # get and post req. for update operation
    path('company/delete/<int:id>/', views.company_delete, name='company_delete'),
    path('company/list/', views.company_list, name='company_list'),  # get req. to retrieve and display all records

    path('products_table/', views.products_table, name="products_table"),
    path('create_product/', views.create_product, name="create_product"),
    path('update_product/<str:pk>', views.update_product, name="update_product"),
    path('delete_product/<str:pk>', views.delete_product, name="delete_product"),

    #json
    path('api/', views.apiOverview, name="api-overview"),
    path('product-list/', views.ProductList, name="product-list"),
    path('product-detail/<str:pk>/', views.ProductDetail, name="product-detail"),
    path('product-create/', views.ProductCreate, name="product-create"),
    path('product-update/<str:pk>/', views.ProductUpdate, name="product-update"),
    path('product-delete/<str:pk>/', views.ProductDelete, name="product-delete"),

]
