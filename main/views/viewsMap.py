from ..utils import *
from ..forms import *

from django.shortcuts import render


# ------------------------------------   Map   ----------------------------------------------------------------------------------

def renderMap(request):
    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    addresses = ShippingAddress.objects.distinct().values("country", "state", "city", "address", "zipcode")

    queryset = list(addresses)

    print(queryset)

    return render(request, 'main/mapBox.html', {'title': 'Map', "addresses": addresses, "items": json.dumps(queryset), 'cartItems': cartItems})
