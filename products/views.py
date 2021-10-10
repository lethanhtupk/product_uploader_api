from rest_framework import generics
from products.models import (
    Product,
    Image,
)
from products.serializers import (
    ProductSerializer,
    ImageSerializer,
)
# Create your views here.


class ProductList(generics.ListCreateAPIView):
    name = 'product-list'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    name = 'product-details'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImageList(generics.ListCreateAPIView):
    name = 'image-list'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_fields = ['product', ]


class ImageDetails(generics.RetrieveUpdateDestroyAPIView):
    name = 'image-details'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
