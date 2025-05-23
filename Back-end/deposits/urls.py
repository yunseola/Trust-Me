from django.urls import path
from . import views
from .views import summarize_product, gpt_recommendation, youtube_videos

urlpatterns = [
    path('save/', views.save_deposit, name='deposit'),
    path('save2/', views.save_saving, name='saving'),
    path('summarize/<int:product_id>/', summarize_product),
    path('recommend/', gpt_recommendation),
    path('youtube/', youtube_videos),
]