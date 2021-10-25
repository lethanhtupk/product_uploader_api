from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from product_uploader_api.custompermission import IsAdminOrReadOnly
from templates.models import (
    Template,
    # Category,
    # Attribute,
    # AttributeOption,
    # Variation,
    # VariationAttribute,
)
from templates.serializers import (
    TemplateSerializer,
    TemplateViewSerializer,
    # CategorySerializer,
    # AttributeSerializer,
    # AttributeOptionSerializer,
    # VariationSerializer,
    # VariationAttributeSerializer,
)

# Create your views here.


# class CategoryList(generics.ListCreateAPIView):
#     name = 'category-list'
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
#     name = 'category-details'
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class TemplateList(generics.ListCreateAPIView):
    name = 'template-list'
    queryset = Template.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    search_fields = ['name', ]
    serializer_class = TemplateSerializer


class TemplateDetails(generics.RetrieveUpdateDestroyAPIView):
    name = 'template-details'
    queryset = Template.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TemplateViewSerializer
        return TemplateSerializer


# class AttributeList(generics.ListCreateAPIView):
#     name = 'attribute-list'
#     queryset = Attribute.objects.all()
#     search_fields = ['name', ]
#     serializer_class = AttributeSerializer


# class AttributeDetails(generics.RetrieveUpdateDestroyAPIView):
#     name = 'attribute-details'
#     queryset = Attribute.objects.all()
#     serializer_class = AttributeSerializer


# class AttributeOptionList(generics.ListCreateAPIView):
#     name = 'attribute-option-list'
#     queryset = AttributeOption.objects.all()
#     serializer_class = AttributeOptionSerializer


# class AttributeOptionDetails(generics.RetrieveUpdateDestroyAPIView):
#     name = 'attribute-option-details'
#     queryset = AttributeOption.objects.all()
#     serializer_class = AttributeOptionSerializer


# class VariationList(generics.ListCreateAPIView):
#     name = 'variation-list'
#     queryset = Variation.objects.all()
#     serializer_class = VariationSerializer


# class VariationDetails(generics.RetrieveUpdateDestroyAPIView):
#     name = 'variation-details'
#     queryset = Variation.objects.all()
#     serializer_class = VariationSerializer


# class VariationAttributeList(generics.ListCreateAPIView):
#     name = 'variation-attribute-list'
#     queryset = VariationAttribute.objects.all()
#     serializer_class = VariationAttributeSerializer


# class VariationAttributeDetails(generics.RetrieveUpdateDestroyAPIView):
#     name = 'variation-attribute-details'
#     queryset = VariationAttribute.objects.all()
#     serializer_class = VariationAttributeSerializer
