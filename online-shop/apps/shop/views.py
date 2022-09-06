import django_filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from .serializers import *
from apps.shop import models
from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework.response import Response
from utils import filters


class ListRetrieveView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    pass


class ProductApiView(ListRetrieveView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, filters.PriceFilter]

    search_fields = ['title', 'description', 'information', 'category__word']

    @action(detail=False)
    def recent_products(self, request):
        recent_products = Product.objects.all().order_by('-created')[:2]
        # page = self.paginate_queryset(recent_products)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recent_products, many=True)
        return Response(serializer.data)


class CategoryApiView(ListRetrieveView):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer


class ContactApiView(generics.CreateAPIView):
    serializer_class = ContactSerializer


class CheckoutApiView(generics.CreateAPIView):
    serializer_class = CheckoutsSerializer


class NewsletterApiView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def perform_create(self, serializer):
        serializer.save()


