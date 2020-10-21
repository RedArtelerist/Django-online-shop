from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.views.generic import TemplateView

from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('jsonApi', TemplateView.as_view(template_name='index.html'), name='jsonApi'),
    path('jsonApi/categories', TemplateView.as_view(template_name='index.html')),
    path('jsonApi/companies', TemplateView.as_view(template_name='index.html')),
    path('jsonApi/products', TemplateView.as_view(template_name='index.html')),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)