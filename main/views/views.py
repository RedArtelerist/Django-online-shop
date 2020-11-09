from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..utils import *
from ..forms import *
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View



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


# ------------------------------------   Register, Login    ----------------------------------------------------------------------------------


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        form.is_active = False
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                firstname = form.cleaned_data.get('first_name')
                lastname = form.cleaned_data.get('last_name')

                Customer.objects.create(user=user, email=email, name=firstname + " " + lastname)

                current_site = request.META['HTTP_HOST']
                print(current_site)
                email_subject ='Activate your account'
                message = render_to_string('main/auth/activate.html',
                                           {
                                               'user': user,
                                               'domain': current_site,
                                               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                               'token': generate_token.make_token(user)

                                           })

                email_message = EmailMessage(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                )

                email_message.send()

                return redirect('verify_email')

        context = {'title': 'Register Account', 'form': form}
        for error in form.errors:
            print(form.errors[error])
        return render(request, 'main/register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'main/login.html', context)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Email was confirmed')
            return redirect('login')
        return render(request, 'main/auth/activate_failed.html', status=401)


def verifyEmailPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'main/auth/verify_email.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')