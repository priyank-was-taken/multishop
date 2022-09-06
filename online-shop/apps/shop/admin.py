from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject']


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'city']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'created']