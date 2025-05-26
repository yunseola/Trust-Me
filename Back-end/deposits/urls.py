from django.urls import path
from . import views
from .views import summarize_product, gpt_recommendation, youtube_videos, get_gold_and_silver_prices, major_exchange_rates, convert_view, historical_exchange_rate, supported_currencies_view

urlpatterns = [
    path('save/', views.save_deposit, name='deposit'),
    path('save2/', views.save_saving, name='saving'),
    path('summarize/<str:product_fin_prdt_cd>/', summarize_product),
    path('recommend/', gpt_recommendation),
    path('youtube/', youtube_videos),
    path("metal/", get_gold_and_silver_prices),
    path("exchange/major/", major_exchange_rates),
    path("exchange/convert/", convert_view),
    path("exchange/historical/", historical_exchange_rate),
    path("exchange/supported/", supported_currencies_view),
]