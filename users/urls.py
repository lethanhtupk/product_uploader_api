from django.urls import path, re_path
from users import views

urlpatterns = [
    path(
        'stores/',
        views.StoreList.as_view(),
        name=views.StoreList.name
    ),
    # re_path(
    #     'categories/(?P<pk>[0-9]+)$',
    #     views.CategoryDetails.as_view(),
    #     name=views.CategoryDetails.name
    # ),
]
