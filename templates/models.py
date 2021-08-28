from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Template(models.Model):
    DRAFT = 'draft'
    PENDING = 'pending'
    PRIVATE = 'private'
    PUBLISH = 'publish'
    STATUS_CHOICES = [
        (DRAFT, 'draft'),
        (PENDING, 'pending'),
        (PRIVATE, 'private'),
        (PUBLISH, 'publish'),
    ]
    VISIBLE = 'visible'
    CATALOG = 'catalog'
    SEARCH = 'search'
    HIDDEN = 'hidden'
    CATALOG_VISIBILITY_CHOICES = [
        (VISIBLE, 'visible'),
        (CATALOG, 'catalog'),
        (SEARCH, 'search'),
        (HIDDEN, 'hidden'),
    ]
    TAXABLE = 'taxable'
    SHIPPING = 'shipping'
    NONE = 'none'
    TAX_STATUS_CHOICES = [
        (TAXABLE, 'taxable'),
        (SHIPPING, 'shipping'),
        (NONE, 'none'),
    ]
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=PUBLISH)
    featured = models.BooleanField(default=False)
    catalog_visibility = models.CharField(
        max_length=255, choices=CATALOG_VISIBILITY_CHOICES, default=VISIBLE)
    description = models.TextField()
    short_description = models.TextField()
    date_on_sale_from = models.DateField(null=True)
    date_on_sale_to = models.DateField(null=True)
    tax_status = models.CharField(
        max_length=255, choices=TAX_STATUS_CHOICES, default=TAXABLE)
    stock_quantity = models.IntegerField(default=1)
    sold_individually = models.BooleanField(default=False)
    tax_class = models.CharField(max_length=255, null=True, default='')
    reviews_allowed = models.BooleanField(default=True)
    position = models.IntegerField(default=0)
    attributes = models.ManyToManyField('Attribute')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AttributeOption(models.Model):
    option = models.CharField(max_length=255)
    attribute = models.ForeignKey(
        to=Attribute, on_delete=models.CASCADE, related_name='options')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.option


class Variation(models.Model):
    template = models.ForeignKey(
        to=Template, on_delete=models.CASCADE, related_name='variations')
    sku = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    tax_class = models.CharField(max_length=255, default="parent")
    sale_price = models.FloatField()
    regular_price = models.FloatField()
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sku


class VariationAttribute(models.Model):
    name = models.ForeignKey(to=Attribute, on_delete=models.PROTECT)
    value = models.ForeignKey(to=AttributeOption, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
