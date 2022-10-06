import django_filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from .serializers import *
from apps.shop import models
from rest_framework import mixins, filters, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from utils import filters


class ListRetrieveView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    pass


class ProductApiView(ListRetrieveView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, filters.CategoryFilter,filters.PriceFilter]

    search_fields = ['title', 'description', 'information', 'category__word']

    @action(detail=False, url_path='', url_name='recent_product')
    def recent_products(self, request):
        recent_products = Product.objects.all().order_by('-created')[:2]
        # page = self.paginate_queryset(recent_products)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recent_products, many=True)
        return Response(serializer.data)


class CategoryApiView(ListRetrieveView):
    parent = None
    queryset = models.Category.objects.filter(parent=parent)
    serializer_class = CategorySerializer


class ContactApiView(generics.CreateAPIView):
    serializer_class = ContactSerializer


class CheckoutApiView(generics.CreateAPIView):
    serializer_class = CheckoutsSerializer


class ShippingApiView(generics.CreateAPIView):
    serializer_class = CheckoutsSerializer


class NewsletterApiView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def perform_create(self, serializer):
        serializer.save()


class ReviewApiView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CartApiView(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReadCartSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     serializer = ReadCartSerializer(instance=serializer.instance)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartDestroyApi(generics.DestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def delete_cart_item(self, request):
        cart_product_id = request.GET.get('cart_product_id')
        Cart.objects.filter(cart__user=request.user.id, id=cart_product_id)
        return Response("item deleted")


