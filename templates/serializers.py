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
        fields = ('code', 'name', 'is_default')


class AttributeSerializer(serializers.ModelSerializer):
    options = AttributeOptionSerializer(many=True, required=False)

    class Meta:
        model = Attribute
        fields = '__all__'


class VariationAttributeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    value = serializers.CharField(max_length=255)

    class Meta:
        model = VariationAttribute
        fields = ['name', 'value']


class VariationAttributeViewSerializer(serializers.ModelSerializer):
    name = AttributeSerializer()
    value = AttributeOptionSerializer()

    class Meta:
        model = VariationAttribute
        fields = '__all__'


class VariationSerializer(serializers.ModelSerializer):
    attributes = VariationAttributeSerializer(many=True)

    class Meta:
        model = Variation
        exclude = ('template',)


class VariationViewSerializer(serializers.ModelSerializer):
    attributes = VariationAttributeViewSerializer(many=True)

    class Meta:
        model = Variation
        exclude = ('template',)


class TemplateSerializer(serializers.ModelSerializer):
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
        attributes_data = validated_data.pop('attributes')
        variations_data = validated_data.pop('variations')
        template = Template.objects.create(**validated_data)

        for attribute_data in attributes_data:
            attribute_data = dict(attribute_data)
            options_data = attribute_data.pop('options')
            attribute, _ = Attribute.objects.get_or_create(
                **attribute_data, template=template)
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
                # TODO: query attribute belong to a specific template
                attribute = Attribute.objects.get(
                    name=attribute_data.get('name'), template=template)
                # TODO: query attribute option belong to specify attribute
                attribute_option = AttributeOption.objects.get(
                    code=attribute_data.get('value'), attribute=attribute)
                VariationAttribute.objects.create(
                    variation=variation, name=attribute, value=attribute_option)

        return template

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get('name', instance.name)
            instance.product_title = validated_data.get(
                'product_title', instance.product_title)
            instance.description = validated_data.get(
                'description', instance.description)

            # TODO: re-create attributes and variations with new data
            attributes_data = validated_data.pop('attributes')
            variations_data = validated_data.pop('variations')

            for attribute_data in attributes_data:
                attribute_data = dict(attribute_data)
                options_data = attribute_data.pop('options')
                attribute, _ = Attribute.objects.get_or_create(
                    **attribute_data, template=instance)
                for option_data in options_data:
                    AttributeOption.objects.get_or_create(
                        attribute=attribute, **dict(option_data))

            for variation_data in variations_data:
                variation_data = dict(variation_data)
                attributes_data = variation_data.pop('attributes')
                variation = Variation.objects.create(
                    template=instance, **variation_data)
                for attribute_data in attributes_data:
                    attribute_data = dict(attribute_data)
                    # TODO: query attribute belong to a specific template
                    attribute = Attribute.objects.get(
                        name=attribute_data.get('name'), template=instance)
                    # TODO: query attribute option belong to specify attribute
                    attribute_option = AttributeOption.objects.get(
                        code=attribute_data.get('value'), attribute=attribute)
                    VariationAttribute.objects.create(
                        variation=variation, name=attribute, value=attribute_option)

            # TODO: delete old attributes
            Attribute.objects.filter(template=instance).delete()
            Variation.objects.filter(template=instance).delete()

        except Exception as e:
            print(e)

        instance.save()
        return instance


class TemplateViewSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True)
    variations = VariationViewSerializer(many=True)

    class Meta:
        model = Template
        fields = '__all__'
