from rest_framework import generics
from templates.models import (
    Category,
    Template,
    Attribute,
    AttributeOption,
    Variation,
    VariationAttribute,
)
from templates.serializers import (
    CategorySerializer,
    TemplateSerializer,
    AttributeSerializer,
    AttributeOptionSerializer,
    VariationSerializer,
    VariationAttributeSerializer,
)

# Create your views here.


class CategoryList(generics.ListCreateAPIView):
    name = 'category-list'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    name = 'category-details'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
