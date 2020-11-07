from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from .views import views
from .views import viewsCRUD
from .views import viewsJsonApi
from .views import viewsMap
from .views import viewsCharts
from .views import viewsRegisterAndLogin



urlpatterns = [

    path('', views.index, name='home'),
    path('store', views.store, name='store'),
    path('json-filter/', views.JsonFilterProductsView.as_view(), name='json_filter'),
    path('about', views.about, name='about'),
    path('product/<str:product_id>', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

    path('category/', viewsCRUD.category_form, name='category_insert'),  # get and post req. for insert operation
    path('category/<int:id>/', viewsCRUD.category_form, name='category_update'),  # get and post req. for update operation
    path('category/delete/<int:id>/', viewsCRUD.category_delete, name='category_delete'),
    path('category/list/', viewsCRUD.category_list, name='category_list'),  # get req. to retrieve and display all records

    path('company/', viewsCRUD.company_form, name='company_insert'),  # get and post req. for insert operation
    path('company/<int:id>/', viewsCRUD.company_form, name='company_update'),  # get and post req. for update operation
    path('company/delete/<int:id>/', viewsCRUD.company_delete, name='company_delete'),
    path('company/list/', viewsCRUD.company_list, name='company_list'),  # get req. to retrieve and display all records

    path('products_table/', viewsCRUD.products_table, name="products_table"),
    path('search-products', csrf_exempt(viewsCRUD.search_products), name="search_products"),
    path('create_product/', viewsCRUD.create_product, name="create_product"),
    path('update_product/<str:pk>', viewsCRUD.update_product, name="update_product"),
    path('delete_product/<str:pk>', viewsCRUD.delete_product, name="delete_product"),

    #json urls products
    path('api/', viewsJsonApi.apiOverview, name="api-overview"),

    path('product-list/', viewsJsonApi.ProductList, name="product-list"),
    path('product-detail/<str:pk>/', viewsJsonApi.ProductDetail, name="product-detail"),
    path('product-create/', viewsJsonApi.ProductView.as_view(), name="product-create"),
    path('product-create/<str:pk>/', viewsJsonApi.ProductView.as_view(), name="product-update"),

    path('product-delete/<str:pk>/', viewsJsonApi.ProductDelete, name="product-delete"),
    
    #json urls category
    path('category-list/', viewsJsonApi.categoryList, name='category-list'),
    path('category-detail/<str:pk>/', viewsJsonApi.categoryDetail, name='category-detail'),
    path('category-create/', viewsJsonApi.categoryCreate, name='category-create'),
    path('category-update/<str:pk>/', viewsJsonApi.categoryUpdate, name='category-update'),
    path('category-delete/<str:pk>/', viewsJsonApi.categoryDelete, name='category-delete'),

    #json urls companies
    path('company-list/', viewsJsonApi.companyList, name='company-list'),
    path('company-detail/<str:pk>/', viewsJsonApi.companyDetail, name='company-detail'),
    path('company-create/', viewsJsonApi.companyCreate, name='company-create'),
    path('company-update/<str:pk>/', viewsJsonApi.companyUpdate, name='company-update'),
    path('company-delete/<str:pk>/', viewsJsonApi.companyDelete, name='company-delete'),


    path("comment/<int:pk>/", views.addComment, name="add-comment"),
    path('comment/<int:pk>/<int:id>/', views.addComment, name='update-comment'),  # get and post req. for update operation
    path('comment/delete/<int:pk>/<int:id>/', views.comment_delete, name='delete-comment'),

    path("review/<int:pk>/", views.addReview, name="add-review"),
    path('review/<int:pk>/<int:id>/', views.addReview, name='update-review'),  # get and post req. for update operation
    path('review/delete/<int:pk>/<int:id>/', views.review_delete, name='delete-review'),

    path('mapBox', viewsMap.renderMap, name='mapBox'),
    path('charts', viewsCharts.renderCharts, name='charts'),

    #RegistrationAndAuthorization

    path('register/', viewsRegisterAndLogin.registerPage, name='register'),
    path('login/', viewsRegisterAndLogin.loginPage, name='login'),
    path('logout/', viewsRegisterAndLogin.logoutUser, name='logout'),


    path('register', views.registerUser, name='register'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),

]
