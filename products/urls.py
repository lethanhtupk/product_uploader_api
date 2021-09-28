from django.urls import path, re_path
from products import views

urlpatterns = [
    path(
        'products/',
        views.ProductList.as_view(),
        name=views.ProductList.name
    ),
    re_path(
        'products/(?P<pk>[0-9]+)$',
        views.ProductDetails.as_view(),
        name=views.ProductDetails.name
    ),
    path(
        'images/',
        views.ImageList.as_view(),
        name=views.ImageList.name
    ),
    re_path(
        'images/(?P<pk>[0-9]+)$',
        views.ImageDetails.as_view(),
        name=views.ImageDetails.name
    ),
]
