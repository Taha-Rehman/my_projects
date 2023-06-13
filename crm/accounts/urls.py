from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('products/', views.products, name="products"),
    path('createorder/<str:pk>/', views.createOrder, name="createorder"),
    path('updateorder/<str:pk>/', views.updateOrder, name="updateorder"),
    path('deleteorder/<str:pk>/', views.deleteOrder, name="deleteorder"),
    path("login/", views.loginpage, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("register/", views.register, name="register"),
    path("user/", views.userPage, name="user"),
    path("createcustomer/", views.createCustomer, name="createcustomer"),
    path("accountsettings/", views.accountSetting, name="accountsetting"),
    # RESETING EAMIL
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),
     
    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]   
