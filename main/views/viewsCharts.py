from ..utils import *
from ..forms import *

from django.shortcuts import render

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

