from django.db import models
import uuid


# Create your models here.


class Category(models.Model):
    woo_id = models.IntegerField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Template(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
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
    SIMPLE = 'simple'
    GROUPED = 'grouped'
    EXTERNAL = 'external'
    VARIABLE = 'variable'
    TYPE_CHOICES = [
        (SIMPLE, 'simple'),
        (GROUPED, 'grouped'),
        (EXTERNAL, 'external'),
        (VARIABLE, 'variable'),
    ]
    type = models.CharField(
        max_length=255, choices=TYPE_CHOICES, default=VARIABLE)
    name = models.CharField(max_length=255, unique=True)
    product_title = models.CharField(max_length=255, default='')
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=PUBLISH)
    featured = models.BooleanField(default=False)
    catalog_visibility = models.CharField(
        max_length=255, choices=CATALOG_VISIBILITY_CHOICES, default=VISIBLE)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    date_on_sale_from = models.DateField(null=True)
    date_on_sale_to = models.DateField(null=True)
    tax_status = models.CharField(
        max_length=255, choices=TAX_STATUS_CHOICES, default=TAXABLE)
    stock_quantity = models.IntegerField(default=1)
    sold_individually = models.BooleanField(default=False)
    tax_class = models.CharField(max_length=255, null=True, default='')
    reviews_allowed = models.BooleanField(default=True)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    template = models.ForeignKey(
        Template, related_name="attributes", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AttributeOption(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255)
    attribute = models.ForeignKey(
        to=Attribute, on_delete=models.CASCADE, related_name='options')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Variation(models.Model):
    IN_STOCK = 'instock'
    OUT_OF_STOCK = 'outofstock'
    STOCK_STATUS_CHOICES = [
        (IN_STOCK, 'instock'),
        (OUT_OF_STOCK, 'outofstock')
    ]
    stock_status = models.CharField(
        max_length=255, choices=STOCK_STATUS_CHOICES, default=IN_STOCK)
    template = models.ForeignKey(
        to=Template, on_delete=models.CASCADE, related_name='variations')
    sku = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    tax_class = models.CharField(max_length=255, default="parent")
    sale_price = models.FloatField()
    regular_price = models.FloatField()
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku


class VariationAttribute(models.Model):
    name = models.ForeignKey(to=Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(to=AttributeOption, on_delete=models.CASCADE)
    variation = models.ForeignKey(
        to=Variation, on_delete=models.CASCADE, related_name='attributes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
