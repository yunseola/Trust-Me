"""
URL configuration for Trust_Me project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from deposits import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('deposits/', include('deposits.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),



    path('products/<str:product_type>/<str:fin_prdt_cd>/', views.product_detail, name='product-detail'),
    path('deposits/save/', views.deposit_list, name='deposit-list'),
    path('deposits/save2/', views.saving_list, name='saving-list'),
    path('deposits/depositoptions/', views.deposit_options_list, name='deposit-options'),
    path('deposits/savingoptions/', views.saving_options_list, name='saving-options'),
]