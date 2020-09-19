from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .decorators import unauthenticated_user, allowed_users

from .models import *
from .utils import *
from .forms import *


# Create your views here.


def index(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    return render(request, 'main/index.html', {'title': 'Main page', 'cartItems': cartItems})


def about(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    return render(request, 'main/about.html', {'cartItems': cartItems})


def store(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    categories = Category.objects.order_by('name')
    products = Product.objects.filter(isActive=True)

    return render(request, 'main/store.html', {'title': 'Store', 'products': products, 'categories': categories, 'cartItems': cartItems})


def product(request, product_id):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    product = Product.objects.get(id=product_id)
    productImages = product.imageitem_set.all()
    return render(request, 'main/product.html', {'title': product.name, 'product': product, 'productImages': productImages, 'cartItems': cartItems})


def cart(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    return render(request, 'main/cart.html', {'title': 'Cart', 'items': items, 'order': order, 'cartItems': cartItems})


def checkout(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    return render(request, 'main/checkout.html', {'title': 'Checkout', 'items': items, 'order': order, 'cartItems': cartItems})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.delete()
        return JsonResponse('Item was added', safe=False)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        print(order.shipping)

    else:
        customer, order = guestData(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        print('Shipping address')
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            country=data['shipping']['country'],
            state=data['shipping']['state'],
            city=data['shipping']['city'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment complete!', safe=False)


#CRUD for Category

@allowed_users(allowed_roles=['admin'])
def category_list(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    categories = Category.objects.order_by('name')

    return render(request, 'main/category_list.html', {'title': 'Categories', 'categories': categories, 'cartItems': cartItems})


@allowed_users(allowed_roles=['admin'])
def category_form(request, id=0):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    if request.method == "GET":
        if id == 0:
            form = CategoryForm()
        else:
            category = Category.objects.get(pk=id)
            form = CategoryForm(instance=category)
        return render(request, "main/category_form.html", {'form': form, 'cartItems': cartItems})
    else:
        if id == 0:
            form = CategoryForm(request.POST)
        else:
            category = Category.objects.get(pk=id)
            form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
        else:
            return render(request, "main/category_form.html", {'form': form, 'cartItems': cartItems})
        return redirect('/category/list')


@allowed_users(allowed_roles=['admin'])
def category_delete(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    return redirect('/category/list')


#CRUD for Company

@allowed_users(allowed_roles=['admin'])
def company_list(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    companies = Company.objects.order_by('name')

    return render(request, 'main/company_list.html', {'title': 'Categories', 'companies': companies, 'cartItems': cartItems})


@allowed_users(allowed_roles=['admin'])
def company_form(request, id=0):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    if request.method == "GET":
        if id == 0:
            form = CompanyForm()
        else:
            company = Company.objects.get(pk=id)
            form = CompanyForm(instance=company)
        return render(request, "main/company_form.html", {'form': form, 'cartItems': cartItems})
    else:
        if id == 0:
            form = CompanyForm(request.POST)
        else:
            company = Company.objects.get(pk=id)
            form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
        else:
            return render(request, "main/company_form.html", {'form': form, 'cartItems': cartItems})
        return redirect('/company/list')


@allowed_users(allowed_roles=['admin'])
def company_delete(request, id):
    company = Company.objects.get(pk=id)
    company.delete()
    return redirect('/company/list')

#CRUD for Product


@allowed_users(allowed_roles=['admin'])
def products_table(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'main/product_crud/products-table.html', context)


@allowed_users(allowed_roles=['admin'])
def create_product(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    form = ProductForm()
    if request.method == 'POST':
        print('POST:', request.POST)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_table')
    context = {'form': form, 'cartItems': cartItems}
    return render(request, 'main/product_crud/create_product.html', context)


@allowed_users(allowed_roles=['admin'])
def update_product(request, pk):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_table')
    context = {'form': form, 'cartItems': cartItems}
    return render(request, 'main/product_crud/create_product.html', context)


@allowed_users(allowed_roles=['admin'])
def delete_product(request, pk):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    product = Product.objects.get(id=pk)
    context = {'item': product, 'cartItems': cartItems}
    if request.method == "POST":
        product.delete()
        return redirect('products_table')
    return render(request, 'main/product_crud/delete_product.html', context)

