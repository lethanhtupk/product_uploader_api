from rest_framework import generics
from rest_framework.permissions import (IsAdminUser, IsAuthenticated)
from product_uploader_api.custompermission import IsAdminOrAssigneeReadOnly
from users.models import Store
from users.serializers import StoreSerializer, StoreViewSerializer

# Create your views here.


class StoreList(generics.ListCreateAPIView):
    name = 'store-list'
    queryset = Store.objects.all()
    permission_classes = (IsAuthenticated,)
    search_fields = ['domain_name', ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StoreViewSerializer
        return StoreSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
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
