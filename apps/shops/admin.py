from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, ProductImage, Specification


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title'
    )
    list_display_links = (
        'indented_title',
    )
    list_filter = (
        'parent',
    )
    search_fields = (
        'title',
        'description'
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'quantity',
        'category'
    )
    list_filter = (
        'category',
    )
    search_fields = (
        'name',
        'description'
    )
    inlines = (
        SpecificationInline,
        ProductImageInline
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'product'
    )
    list_filter = (
        'product',
    )
    search_fields = (
        'product__name',
    )


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'product'
    )
    list_filter = (
        'product',
    )
    search_fields = (
        'product__name',
    )
