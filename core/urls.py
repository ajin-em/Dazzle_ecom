from django.urls import path
from .views import *
from store.urls import *

urlpatterns = [
    path('signin/',SignIn.as_view(),name='signin'),
    path('verification/' ,VerifyOTP.as_view(), name='verify_otp'),
    path('register/',CreateUser.as_view(),name='register'),
    path('resendotp/',ResendOTP.as_view(),name='resend'),   
    path('signout/',SignOut.as_view(),name='logout'),
    path('profile/',UserProfileView.as_view(), name='profile'),
    path('manage_address/',UserManageAddress.as_view(), name='manage_address'),
    path('add_address/',UserAddAddress.as_view(), name='add_address'),
    path('update_address/<str:pk>/',UserUpdateAddress.as_view(), name='update_address'),
    path('delete_address/<str:pk>/',UserDeleteAddress.as_view(), name='delete_address'),
]

    