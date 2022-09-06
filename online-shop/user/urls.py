from user import views
from django.urls import path, include

urlpatterns = [

    path('signup/', views.SignupApiView.as_view(), name='signup'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    # path('email/', views.EmailApiView.as_view(), name='login'),
]
