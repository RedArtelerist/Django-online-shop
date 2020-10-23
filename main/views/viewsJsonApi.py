from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from ..serializers import *
from ..forms import *

from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


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
