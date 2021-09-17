from templates.serializers import CategorySerializer
from django.urls import path, re_path
from templates import views

urlpatterns = [
    path(
        'categories/',
        views.CategoryList.as_view(),
        name=views.CategoryList.name
    ),
    # re_path(
    #     'categories/(?P<pk>[0-9]+)$',
    #     views.CategoryDetails.as_view(),
    #     name=views.CategoryDetails.name
    # ),
    path(
        'templates/',
        views.TemplateList.as_view(),
        name=views.TemplateList.name
    ),
    re_path(
        'templates/(?P<pk>[0-9]+)$',
        views.TemplateDetails.as_view(),
        name=views.TemplateDetails.name
    ),
    path(
        'attributes/',
        views.AttributeList.as_view(),
        name=views.AttributeList.name
    ),
    re_path(
        'attributes/(?P<pk>[0-9]+)$',
        views.AttributeDetails.as_view(),
        name=views.AttributeDetails.name
    ),
    path(
        'attribute-options/',
        views.AttributeOptionList.as_view(),
        name=views.AttributeOptionList.name
    ),
    re_path(
        'attribute-options/(?P<pk>[0-9]+)$',
        views.AttributeOptionDetails.as_view(),
        name=views.AttributeOptionDetails.name
    ),
]
