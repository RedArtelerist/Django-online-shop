from django.views.generic import ListView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.exceptions import MethodNotAllowed, APIException
from rest_framework.response import Response
import json
import datetime
from django.conf import settings
from django.urls import reverse

from .decorators import unauthenticated_user, allowed_users

from .serializers import *
from .utils import *
from .forms import *

from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView




from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse


# ------------------------------------   Pages   ----------------------------------------------------------------------------------

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
    companies = Company.objects.order_by('name')
    countries = Company.objects.order_by('country').values('country').distinct()
    products = Product.objects.filter(isActive=True)

    prices = []
    for product in products:
        prices.append(product.discount_price)
    max_price = max(prices)
    min_price = min(prices)
    print(min_price, " ", max_price)

    """cat_names = []
    comp_names = []
    comp_countries = []
    for name in Category.objects.values("id"):
        cat_names.append(name['id'])

    for name in Company.objects.values("id"):
        comp_names.append(name['id'])

    for country in Company.objects.values("country").distinct():
        comp_countries.append(country['country'])

    list_category = request.GET.getlist("category")
    list_company = request.GET.getlist("company")
    list_country = request.GET.getlist("country")

    minprice = request.GET.getlist("minprice")
    maxprice = request.GET.getlist("maxprice")
    print(minprice, ' ', maxprice)
    if minprice == [''] or minprice == []:
        minprice = min_price
    else: minprice = minprice[0]
    if maxprice == [''] or maxprice == []:
        maxprice = max_price
    else:maxprice = maxprice[0]
    print(minprice, ' ', maxprice)

    queryset = []
    if len(list_category) == 0:
        list_category = cat_names
    if len(list_company) == 0:
        list_company = comp_names
    if len(list_country) == 0:
        list_country = comp_countries

    queryset = Product.objects.filter(
        isActive=True,
        category__in=list_category,
        company__in=list_company,
        company__country__in=list_country,
    ).distinct()

    products_queryset = []
    for product in queryset:
        if float(minprice) - 0.01 <= product.discount_price <= float(maxprice) + 0.01:
            products_queryset.append(product)"""

    return render(request, 'main/store.html',
                  {'title': 'Store',
                   'products': products,
                   'maxprice': max_price,
                   'minprice': min_price,
                   'categories': categories,
                   'companies': companies,
                   'countries': countries,
                   'cartItems': cartItems})


# ------------------------------------   Filter Products   ----------------------------------------------------------------------------------

class JsonFilterProductsView(ListView):
    def get_queryset(self):
        products = Product.objects.filter(isActive=True)

        prices = []
        for product in products:
            prices.append(product.discount_price)
        max_price = max(prices)
        min_price = min(prices)

        cat_names = []
        comp_names = []
        comp_countries = []
        for name in Category.objects.values("id"):
            cat_names.append(name['id'])

        for name in Company.objects.values("id"):
            comp_names.append(name['id'])

        for country in Company.objects.values("country").distinct():
            comp_countries.append(country['country'])

        list_category = self.request.GET.getlist("category")
        list_company = self.request.GET.getlist("company")
        list_country = self.request.GET.getlist("country")

        minprice = self.request.GET.getlist("minprice")
        maxprice = self.request.GET.getlist("maxprice")
        print(minprice, ' ', maxprice)
        if minprice == [''] or minprice == []:
            minprice = min_price
        else:
            minprice = minprice[0]
        if maxprice == [''] or maxprice == []:
            maxprice = max_price
        else:
            maxprice = maxprice[0]
        print(minprice, ' ', maxprice)

        if len(list_category) == 0:
            list_category = cat_names
        if len(list_company) == 0:
            list_company = comp_names
        if len(list_country) == 0:
            list_country = comp_countries

        queryset = Product.objects.annotate(
            discount_price=ExpressionWrapper((Value(1.0) - F('discount') / Value(100.0)) * F('price'),
                                             output_field=FloatField()),
            count_review=Count('review'),
            average_review=Avg('review__rate')).filter(
            isActive=True,
            category__in=list_category,
            company__in=list_company,
            company__country__in=list_country,
        ).distinct().values("id", "image", "name", "price", "discount", "shortSpecifications", "discount_price",
                            "count_review", "average_review")

        products_queryset = []
        for product in queryset:
            if float(minprice) - 0.01 <= product['discount_price'] <= float(maxprice) + 0.01:
                products_queryset.append(product)

        print(products_queryset)

        return products_queryset

    def get(self, request, *args, **kwargs):
        """cookieData = cartData(request)
        cartItems = cookieData['cartItems']

        products = Product.objects.filter(isActive=True)
        prices = []
        for product in products:
            prices.append(product.discount_price)
        max_price = max(prices)
        min_price = min(prices)

        categories = Category.objects.order_by('name')
        companies = Company.objects.order_by('name')
        countries = Company.objects.order_by('country').values('country').distinct()"""

        queryset = list(self.get_queryset())
        for q in queryset:
            if q['average_review'] is None:
                q['average_review'] = 0.00
            q['average_review'] = format(q['average_review'], '.2f')
            q['discount_price'] = format(q['discount_price'], '.2f')

        return JsonResponse({"products": queryset})


def product(request, product_id):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    product = Product.objects.get(id=product_id)
    productImages = product.imageitem_set.all()
    return render(request, 'main/product.html',
                  {'title': product.name,
                   'product': product,
                   'productImages': productImages,
                   'cartItems': cartItems,
                   'user': request.user})


"""class FilterProductsView(ListView):
    # paginate_by = 5

    def get_queryset(self):
        cookieData = cartData(self.request)
        cartItems = cookieData['cartItems']

        categories = Category.objects.order_by('name')
        companies = Company.objects.order_by('name')
        countries = Company.objects.order_by('country').values('country').distinct()

        queryset = Product.objects.filter(
            Q(category__in=self.request.GET.getlist("category")) |
            Q(company__in=self.request.GET.getlist("company"))
        ).distinct()
        # return queryset
        return render(self.request, 'main/store.html',
                      {'title': 'Store', 'products': queryset,
                       'categories': categories,
                       'companies': companies,
                       'countries': countries,
                       'cartItems': cartItems})"""


# ------------------------------------   Cart and Checkout   ----------------------------------------------------------------------------------


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

    return render(request, 'main/checkout.html',
                  {'title': 'Checkout', 'items': items, 'order': order, 'cartItems': cartItems})


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

    if order.shipping:
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


# ------------------------------------   Comment CRUD   ----------------------------------------------------------------------------------


def addComment(request, pk, id=0):
    product = Product.objects.get(id=pk)
    parent = None

    if id == 0:
        form = CommentForm(request.POST)
    else:
        comment = Comment.objects.get(pk=id)
        parent = comment.parent
        form = CommentForm(request.POST, instance=comment)

    if form.is_valid():
        form = form.save(commit=False)
        if request.user.is_authenticated:
            form.user = request.user
            form.name = request.user.username
            form.email = request.user.email

        form.parent = parent
        if request.POST.get("parent", None) and id == 0:
            form.parent_id = int(request.POST.get("parent"))
        form.product = product
        form.data_added = datetime.datetime.now()
        form.save()

    return redirect('product', product_id=pk)


def comment_delete(request, pk, id):
    comment = Comment.objects.get(pk=id)
    comment.delete()
    return redirect('product', product_id=pk)


# ------------------------------------   Review CRUD   ----------------------------------------------------------------------------------


def addReview(request, pk, id=0):
    product = Product.objects.get(id=pk)

    if id == 0:
        form = ReviewForm(request.POST)
    else:
        review = Review.objects.get(pk=id)
        form = ReviewForm(request.POST, instance=review)

    if form.is_valid():
        form = form.save(commit=False)
        if request.user.is_authenticated:
            form.user = request.user

        form.product = product
        form.data_added = datetime.datetime.now()
        form.save()

    return redirect('product', product_id=pk)


def review_delete(request, pk, id):
    review = Review.objects.get(pk=id)
    review.delete()
    return redirect('product', product_id=pk)


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


# ------------------------------------   json API Products   ----------------------------------------------------------------------------------


# @allowed_users(allowed_roles=['admin'])
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'ProductList': '/product-list/',
        'DetailViewProduct': '/product-detail/<str:pk>/',
        'CreateProduct': '/product-create/',
        'UpdateProduct': '/product-update/<str:pk>/',
        'DeleteProduct': '/product-delete/<str:pk>/',
    }
    return Response(api_urls)



# @allowed_users(allowed_roles=['admin'])
@api_view(['GET'])
def ProductList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



# @allowed_users(allowed_roles=['admin'])
@api_view(['GET'])
def ProductDetail(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except:
        return Response(status=404)


class ProductView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk=0, *args, **kwargs):
        if pk == 0:
            product_serializer = ProductSerializer(data=request.data)
        else:
            product = Product.objects.get(id=pk)
            product_serializer = ProductSerializer(instance=product, data=request.data, many=False, partial=True)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data)
        else:
            print('error', product_serializer.errors)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @allowed_users(allowed_roles=['admin'])
@api_view(['DELETE'])
def ProductDelete(request, pk, ):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return Response("OK!")
    except:
        raise APIException("Error!")


# ------------------------------------   json API Category   ----------------------------------------------------------------------------------

# @allowed_users(allowed_roles=['admin'])
@api_view(['GET'])
def categoryList(request):
    categories = Category.objects.order_by('-id')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# @allowed_users(allowed_roles=['admin'])
@api_view(['GET'])
def categoryDetail(request, pk):
    try:
        categories = Category.objects.get(id=pk)
        serializer = CategorySerializer(categories, many=False)
        return Response(serializer.data)
    except:
        raise APIException("Detail Error")


# @allowed_users(allowed_roles=['admin'])
@api_view(['POST'])
def categoryCreate(request):
    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data)


# @allowed_users(allowed_roles=['admin'])
@api_view(['PUT'])
def categoryUpdate(request, pk):
    try:
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(instance=category, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)
    except:
        raise APIException("Update Error")


# @allowed_users(allowed_roles=['admin'])
@api_view(['DELETE'])
def categoryDelete(request, pk):
    try:
        category = Category.objects.get(id=pk)
        category.delete()
        return Response("Ok")
    except:
        raise APIException("Delete Error")


# ------------------------------------   json API Company   ----------------------------------------------------------------------------------

# @allowed_users(allowed_roles=['admin'])
@api_view(['GET'])
def companyList(request):
    companies = Company.objects.order_by('-id')
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


# @allowed_users(allowed_roles=['admin'])
@api_view(['GET'])
def companyDetail(request, pk):
    try:
        companies = Company.objects.get(id=pk)
        serializer = CompanySerializer(companies, many=False)
        return Response(serializer.data)
    except:
        raise APIException("Detail Error")


# @allowed_users(allowed_roles=['admin'])
@api_view(['POST'])
def companyCreate(request):
    serializer = CompanySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data)


# @allowed_users(allowed_roles=['admin'])
@api_view(['PUT'])
def companyUpdate(request, pk):
    try:
        company = Company.objects.get(id=pk)
        serializer = CompanySerializer(instance=company, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)
    except:
        raise APIException("Update Error")


# @allowed_users(allowed_roles=['admin'])
@api_view(['DELETE'])
def companyDelete(request, pk):
    try:
        company = Company.objects.get(id=pk)
        company.delete()
        return Response("Ok")
    except:
        raise APIException("Delete Error")


# ------------------------------------   Map   ----------------------------------------------------------------------------------

def renderMap(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    addresses = ShippingAddress.objects.distinct().values("country", "state", "city", "address", "zipcode")

    queryset = list(addresses)

    print(queryset)

    return render(request, 'main/mapBox.html', {'title': 'Map', "addresses": addresses, "items": json.dumps(queryset), 'cartItems': cartItems})


# ------------------------------------   Chart   ----------------------------------------------------------------------------------
def renderCharts(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    orders = Order.objects.filter(complete=True)
    products_by_orders = dict()
    company_by_orders = dict()
    categories_by_orders = dict()

    for order in orders:
        items = order.orderitem_set.all()
        for item in items:
            key1 = item.product.name
            products_by_orders[key1] = products_by_orders.get(key1, 0) + item.quantity

            key2 = item.product.category.name
            company_by_orders[key2] = company_by_orders.get(key2, 0) + item.quantity

            key3 = item.product.company.name
            categories_by_orders[key3] = categories_by_orders.get(key3, 0) + item.quantity

    list = [products_by_orders, company_by_orders, categories_by_orders]
    print(list)

    return render(request, 'main/Charts.html', {'title': 'Charts', 'data': json.dumps(list), 'cartItems': cartItems})

