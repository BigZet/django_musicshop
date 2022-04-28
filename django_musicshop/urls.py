"""django_musicshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from musicshop.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name = "admin"),
    path('', CatalogPage.as_view(), name = "index"),
    path('catalog/category/<slug:category_slug>', CatalogPage.as_view(), name = 'catalog'),
    path('catalog/category/', CatalogPage.as_view(), name = 'catalog_category_empty'),
    path('catalog/', CatalogPage.as_view(), name = 'catalog_empty'),
    path('cart/', CartPage.as_view(), name = 'cart'),
    path('catalog/category/<slug:category_slug>/<slug:item_slug>', ItemPage.as_view(), name='item_about'),
    path('login/', LoginUser.as_view(), name = "login")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
