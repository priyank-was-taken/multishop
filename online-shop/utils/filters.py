import django_filters
from django.db.models import Max
from django.shortcuts import render
from rest_framework import status
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response

from apps.shop import models


class PriceFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if 'min_price' in request.GET:
            filter_price1 = request.GET.get('min_price')
            filter_price2 = request.GET.get('max_price')
            if filter_price1 == '':
                filter_price1 = 0
            if filter_price2 == '':
                filter_price2 = models.Product.objects.all().aggregate(Max('price'))
            my_products = models.Product.objects.filter(new_price__range=(filter_price1, filter_price2))
            return my_products

        else:
            return queryset


# class PriceFilter(django_filters.FilterSet):
#     min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
#     max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
#
#     class Meta:
#         model = models.Product
#         fields = ['min_price', 'max_price']
