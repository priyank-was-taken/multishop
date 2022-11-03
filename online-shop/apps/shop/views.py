import django_filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from user.models import User
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
    filter_backends = [SearchFilter, filters.PriceFilter]

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


class ListRetrieveDeleteCreateView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                                   mixins.CreateModelMixin, GenericViewSet):
    pass


class CartApiView(ListRetrieveDeleteCreateView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = ReadCartSerializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(pk=request.data['product'])
        user = User.objects.get(pk=request.data['user'])
        cart_product = Cart.objects.filter(user=user, product=product)
        if cart_product:
            instance = cart_product.last()
            instance.quantity += int(request.data['quantity'])
            instance.save()
        else:
            quantity = request.data['quantity']
            user = User.objects.get(pk=request.data['user'])
            cart = Cart.objects.create(user=user, product=product, quantity=quantity)
            serializer = CartSerializer(cart, many=True)
            # serializer.save(user=self.request.user)
        return Response(serializer.data)


# -------------------just for testing--------------------


class TestApiView(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
