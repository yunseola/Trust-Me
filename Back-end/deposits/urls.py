from django.urls import path
from . import views

urlpatterns = [
    path('save/', views.save_deposit, name='deposit'),
    path('save2/', views.save_saving, name='saving'),
]