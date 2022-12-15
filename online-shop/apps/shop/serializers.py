from django.conf import settings
# from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.shop.models import Category, Product, Contact, Checkout, Newsletter, Review, Cart, Test, Wishlist
from django.contrib.auth.password_validation import validate_password


class ReadProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price', 'old_price']


class CategorySerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True, many=True)
    product_count = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'word', 'image', 'product_count', 'parent', 'children', 'product']

    def get_product_count(self, obj):
        return obj.product.count()

    def get_product(self):
        return

    def get_children(self, obj):
        data = obj.get_children()
        return CategorySerializer(data, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price', 'old_price', 'description', 'information', 'size', 'color',
                  'category']
        # fields = ['id', 'user', 'status', 'created', 'modified', 'activate_date', 'deactivate_date', 'title', 'image',
        #           'price', 'category']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class CheckoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

    def validate(self, attrs):
        email = super().validate(attrs)
        key = attrs['email']
        send_mail(
            'email verification',
            f"you are registered",
            settings.EMAIL_HOST_USER,
            [key],
            fail_silently=False,
        )
        return email


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'star', 'text', 'name', 'email', 'created']

    # avg_rating = serializers.SerializerMethodField()
    #
    # def get_avg_rating(self, ob):
    #     # reverse lookup on Reviews using item field
    #     return ob.star.aggregate(Avg('star'))['star__avg']


class CartSerializer(serializers.ModelSerializer):
    # product_id = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='title', write_only=True)
    # user = serializers.StringRelatedField()
    # product_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'net_price', 'created', 'modified', 'quantity']

    # def update(self, instance, validated_data):
    #     if "quantity" in validated_data:
    #         instance.quantity = validated_data.get('quantity')
    #         instance.save()
    #     return super().update(instance, validated_data)

    # def get_product_count(self, obj):
    #     return obj.product.count()


class ReadCartProductSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'created', 'modified']


# class ReadCartSerializer(serializers.ModelSerializer):
#     product = ReadCartProductSerializer(read_only=True)
#
#     # user = serializers.StringRelatedField()
#
#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'product', 'created', 'modified']


# -------------------just for testing--------------------
class TestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                     style={'input_type': 'password'})

    class Meta:
        model = Test
        fields = ['id', 'name', 'email', 'password', 'message']
