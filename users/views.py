from rest_framework import generics, request
from rest_framework import permissions
from rest_framework.permissions import (IsAuthenticated)
from product_uploader_api.custompermission import ADMIN, SUPER_ADMIN, HasHigherPrivilege, IsAdmin, IsAdminOrAssigneeReadOnly
from users.models import CustomUser, Store
from users.serializers import PublicUserForViewSerializer, PublicUserSerializer, StoreSerializer, StoreViewSerializer

# Create your views here.


class StoreList(generics.ListCreateAPIView):
    name = 'store-list'
    queryset = Store.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)
    search_fields = ['domain_name', ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StoreViewSerializer
        return StoreSerializer

    def get_queryset(self):
        if self.request.user.role in [ADMIN, SUPER_ADMIN]:
            return Store.objects.all()
        else:
            return Store.objects.filter(users=self.request.user)


class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'store-details'
    queryset = Store.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrAssigneeReadOnly)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StoreViewSerializer
        return StoreSerializer


class UserList(generics.ListCreateAPIView):
    name = 'user-list'
    permission_classes = (IsAuthenticated, IsAdmin)
    search_fields = ['username', ]

    def get_queryset(self):
        print(self.request.user.role)
        if (self.request.user.role == 2):
            return CustomUser.objects.filter(role=1)
        elif (self.request.user.role == 3):
            return CustomUser.objects.filter(role__in=[1, 2])
        # normal user.
        return []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PublicUserForViewSerializer
        return PublicUserSerializer


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    name = 'user-details'
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin, HasHigherPrivilege)
    serializer_class = PublicUserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PublicUserForViewSerializer
        return PublicUserSerializer
