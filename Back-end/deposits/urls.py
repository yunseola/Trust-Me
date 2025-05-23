from django.urls import path
from . import views
from .views import summarize_product

urlpatterns = [
    path('save/', views.save_deposit, name='deposit'),
    path('save2/', views.save_saving, name='saving'),
    path('summarize/<int:product_id>/', summarize_product)
]