from rest_framework import generics
from users.models import Store
from users.serializers import StoreSerializer, StoreViewSerializer

# Create your views here.


class StoreList(generics.ListCreateAPIView):
    name = 'store-list'
    queryset = Store.objects.all()
    search_fields = ['domain_name', ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StoreViewSerializer
        return StoreSerializer


class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'store-details'
    queryset = Store.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StoreViewSerializer
        return StoreSerializer
