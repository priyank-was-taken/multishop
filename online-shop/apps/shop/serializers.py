from django.conf import settings
# from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from user import models
from apps.shop.models import Category, Product, Contact, Checkout, Newsletter
from django.contrib.auth.password_validation import validate_password


class ReadProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'price', 'description', 'information', 'size', 'color', 'category']
        # fields = ['id', 'user', 'status', 'created', 'modified', 'activate_date', 'deactivate_date', 'title', 'image',
        #           'price', 'category']


class CategorySerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True, many=True)
    product_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'word', 'image', 'product_count', 'product']

    def get_product_count(self, obj):
        return obj.product.count()


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class CheckoutsSerializer(serializers.ModelSerializer):

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

    # def create(self, validated_data):
    #     instance = super(NewsletterSerializer, self).create(validated_data)
    #     email = format(instance.email)
    #
    #     is_exists = Newsletter.objects.filter(email=email).exists()
    #     if is_exists:
    #         raise ValidationError('Email exists')
    #
    #     else:
    #         send_mail(
    #             'email verification',
    #             f"you are registered",
    #             settings.EMAIL_HOST_USER,
    #             [email],
    #             fail_silently=False,
    #         )
    #     return instance
