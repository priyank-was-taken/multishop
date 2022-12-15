import django_filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.status import *
from user.models import User
from apps.shop import serializers as shop_serializer
from apps.shop import models
from rest_framework import mixins, filters, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from utils import filter
from rest_framework import filters


class ListRetrieveView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    pass


class ProductApiView(ListRetrieveView):
    queryset = models.Product.objects.all()
    serializer_class = shop_serializer.ProductSerializer
    filter_backends = [SearchFilter, filter.PriceFilter]
    # permission_classes =

    search_fields = ['title', 'description', 'information', 'category__word']

    @action(detail=False, url_path='recent_product')
    def recent_products(self, request):
        recent_products = models.Product.objects.all().order_by('-created')[:4]
        # page = self.paginate_queryset(recent_products)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recent_products, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='recent_product/(?P<pk>\d+)')
    def recent_products_detail(self, request, pk):
        id = int(self.kwargs['pk'])
        recent_products = [*models.Product.objects.order_by('-created')[:4].values_list("id", flat=True)]
        if id in recent_products:
            recent_products = models.Product.objects.get(pk=id)
            serializer = self.get_serializer(recent_products, context={'request': request})
            return Response(serializer.data)
        else:
            return Response(status=HTTP_404_NOT_FOUND)


class CategoryApiView(ListRetrieveView):
    parent = None
    queryset = models.Category.objects.filter(parent=parent)
    serializer_class = shop_serializer.CategorySerializer


class ContactApiView(generics.CreateAPIView):
    serializer_class = shop_serializer.ContactSerializer


class CheckoutApiView(generics.CreateAPIView):
    serializer_class = shop_serializer.CheckoutsSerializer


class ShippingApiView(generics.CreateAPIView):
    serializer_class = shop_serializer.CheckoutsSerializer


class NewsletterApiView(generics.CreateAPIView):
    queryset = models.Newsletter.objects.all()
    serializer_class = shop_serializer.NewsletterSerializer

    def perform_create(self, serializer):
        serializer.save()


class ReviewApiView(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = shop_serializer.ReviewSerializer


class ListRetrieveUpdateDeleteCreateView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                                         mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    pass


class CartApiView(ListRetrieveUpdateDeleteCreateView):
    queryset = models.Cart.objects.all()
    serializer_class = shop_serializer.CartSerializer
    filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['-created']
    ordering = ["created"]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = shop_serializer.CartSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = shop_serializer.ReadCartProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = shop_serializer.ReadCartProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = models.Product.objects.get(pk=request.data['product'])
        user = User.objects.get(pk=request.data['user'])
        cart_product = models.Cart.objects.filter(user=user, product=product)
        if cart_product:
            instance = cart_product.last()
            instance.quantity += int(request.data['quantity'])
            instance.save()
        else:
            quantity = request.data['quantity']
            user = User.objects.get(pk=request.data['user'])
            cart = models.Cart.objects.create(user=user, product=product, quantity=quantity)
            serializer = shop_serializer.ReadCartProductSerializer(cart)

        return Response(serializer.data)


class WishlistApiView(ListRetrieveUpdateDeleteCreateView):
    queryset = models.Wishlist.objects.all()
    serializer_class = shop_serializer.WishlistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = models.Product.objects.get(pk=request.data['product'])
        user = User.objects.get(pk=request.data['user'])
        wishlist_product = models.Wishlist.objects.filter(user=user, product=product)
        if wishlist_product:
            return Response('product already in wishlist')
        else:
            user = User.objects.get(pk=request.data['user'])
            wishlist = models.Wishlist.objects.create(user=user, product=product)
            serializer = shop_serializer.WishlistSerializer(wishlist)

        return Response(serializer.data)


# -------------------just for testing--------------------


class TestApiView(ModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = shop_serializer.TestSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
