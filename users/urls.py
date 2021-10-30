from django.urls import path, re_path
from users import views

urlpatterns = [
    path(
        'stores/',
        views.StoreList.as_view(),
        name=views.StoreList.name
    ),
    path(
        'stores/<uuid:pk>',
        views.StoreDetail.as_view(),
        name=views.StoreDetail.name
    ),
    path(
        'users/',
        views.UserList.as_view(),
        name=views.UserList.name
    ),
    re_path(
        'users/(?P<pk>[0-9]+)$',
        views.UserDetails.as_view(),
        name=views.UserDetails.name
    )
]
