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


class AttributeOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeOption
        fields = ('option',)


class AttributeSerializer(serializers.ModelSerializer):
    options = AttributeOptionSerializer(many=True)

    class Meta:
        model = Attribute
        fields = '__all__'

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        attribute = Attribute.objects.create(**validated_data)
        for option_data in options_data:
            AttributeOption.objects.create(attribute=attribute, **option_data)
        return attribute


class VariationAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariationAttribute
        exclude = ('variation',)


class VariationSerializer(serializers.ModelSerializer):
    attributes = VariationAttributeSerializer(many=True)

    class Meta:
        model = Variation
        exclude = ('template',)


class TemplateSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    attributes = AttributeSerializer(many=True)
    variations = VariationSerializer(many=True)

    class Meta:
        model = Template
        fields = '__all__'

    def validate(self, data):
        attributes = data['attributes']
        has_primary_attribute = False
        for attribute in attributes:
            is_primary = dict(attribute).get('is_primary', None)
            if has_primary_attribute and is_primary:
                raise serializers.ValidationError({
                    'attributes': {
                        'is_primary': 'Only accepts 1 primary attribute'
                    }
                })
            elif is_primary:
                has_primary_attribute = True
        return data

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        attributes_data = validated_data.pop('attributes')
        variations_data = validated_data.pop('variations')
        template = Template.objects.create(**validated_data)
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(
                **dict(category_data))
            template.categories.add(category)

        for attribute_data in attributes_data:
            attribute_data = dict(attribute_data)
            options_data = attribute_data.pop('options')
            attribute, _ = Attribute.objects.get_or_create(
                **attribute_data)
            template.attributes.add(attribute)
            for option_data in options_data:
                AttributeOption.objects.get_or_create(
                    attribute=attribute, **dict(option_data))

        for variation_data in variations_data:
            variation_data = dict(variation_data)
            attributes_data = variation_data.pop('attributes')
            variation = Variation.objects.create(
                template=template, **variation_data)
            for attribute_data in attributes_data:
                attribute_data = dict(attribute_data)
                attribute = Attribute.objects.get(
                    pk=attribute_data.get('name'))
                attribute_option = AttributeOption.objects.get(
                    pk=attribute_data.get('value'))
                VariationAttribute.objects.create(
                    variation=variation, name=attribute, value=attribute_option)

        return template
