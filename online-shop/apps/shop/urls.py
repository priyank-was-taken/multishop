from rest_framework import routers
from apps.shop import views
from django.urls import path, include

routers = routers.DefaultRouter()

routers.register('product', views.ProductApiView, basename='shop')
routers.register('category', views.CategoryApiView, basename='category')
routers.register('cart', views.CartApiView, basename='cart')
routers.register('test', views.TestApiView, basename='test')

urlpatterns = [
    path('', include(routers.urls)),
    path('contact/', views.ContactApiView.as_view(), name='contact'),
    path('checkout/', views.CheckoutApiView.as_view(), name='checkout'),
    path('shipping/', views.ShippingApiView.as_view(), name='billing'),
    path('newsletter/', views.NewsletterApiView.as_view(), name='newsletter'),
    path('review/', views.ReviewApiView.as_view(), name='review'),
]
