from re import L
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from templates.models import (
    Category,
    Template,
    Attribute,
    AttributeOption,
    Variation,
    VariationAttribute
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeOption
        fields = '__all__'


class VariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variation
        fields = '__all__'


class VariationAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariationAttribute
        fields = '__all__'
