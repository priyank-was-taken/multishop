from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']


@admin.register(Category)
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "word"
    list_display = ('tree_actions', 'indented_title',
                    )
    list_display_links = ('indented_title',)

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #
    #     # Add cumulative product count
    #     qs = Category.objects.add_related_count(
    #             qs,
    #             Product,
    #             'category',
    #             'products_cumulative_count',
    #             cumulative=True)
    #
    #     # Add non cumulative product count
    #     qs = Category.objects.add_related_count(qs,
    #              Product,
    #              'category',
    #              'products_count',
    #              cumulative=False)
    #     return qs
    #
    # def related_products_count(self, instance):
    #     return instance.products_count
    # related_products_count.short_description = 'Related products (for this specific category)'
    #
    # def related_products_cumulative_count(self, instance):
    #     return instance.products_cumulative_count
    # related_products_cumulative_count.short_description = 'Related products (in tree)'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'old_price', 'price']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject']


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'city']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'created']