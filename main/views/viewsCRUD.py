from django.http import JsonResponse
from django.shortcuts import render, redirect
from ..decorators import  allowed_users
from ..utils import *
from ..forms import *
from django.shortcuts import render


# ------------------------------------   CRUD for Category   ----------------------------------------------------------------------------------


@allowed_users(allowed_roles=['admin'])
def category_list(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    categories = Category.objects.order_by('name')

    return render(request, 'main/category_list.html',
                  {'title': 'Categories', 'categories': categories, 'cartItems': cartItems})


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


# ------------------------------------   CRUD for Company   ----------------------------------------------------------------------------------


@allowed_users(allowed_roles=['admin'])
def company_list(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    companies = Company.objects.order_by('name')

    return render(request, 'main/company_list.html',
                  {'title': 'Categories', 'companies': companies, 'cartItems': cartItems})


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


# ------------------------------------   CRUD for Product   ----------------------------------------------------------------------------------
def search_products(request):
    if request.method == 'POST':

        print(request)
        search_str = json.loads(request.body).get('searchText')
        products = Product.objects.filter(isActive=True, name__icontains=search_str)\
            .values("id", "image", "name", "price", "discount", "year", "shortSpecifications",
                    "isActive", "digital", "company__name", "category__name")

        data = products.values()

        return JsonResponse(list(products), safe=False)


@allowed_users(allowed_roles=['admin'])
def products_table(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    if 'term' in request.GET:
        qs = Product.objects.filter(isActive=True, name__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.name)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)

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

