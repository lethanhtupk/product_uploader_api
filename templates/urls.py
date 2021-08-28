from templates.serializers import CategorySerializer
from django.urls import path, re_path
from templates import views

urlpatterns = [
    path(
        'categories/',
        views.CategoryList.as_view(),
        name=views.CategoryList.name
    ),
    re_path(
        'categories/(?P<pk>[0-9]+)$',
        views.CategoryDetails.as_view(),
        name=views.CategoryDetails.name
    )
]
