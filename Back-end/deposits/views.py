from django.conf import settings
from rest_framework.response import Response
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts
from .serializers import DepositProductsSerializerD, DepositProductsSerializerC, DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializerD, SavingProductsSerializerC, SavingProductsSerializer, SavingOptionsSerializer
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from deposits.models import DepositProducts
from .services.summary import summarize_deposit_product
from .services.youtube import search_youtube_videos
from .services.metal import fetch_gold_or_silver_data
from .services.exchange import (
    get_major_exchange_rates,
    convert_currency,
    get_historical_rate,
    get_supported_currencies
)

from django.db.models import Count, Q

DEPOSIT_BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

# Create your views here.

@api_view(['GET'])
def save_deposit(request): # models에 저장하는 함수
    URL = DEPOSIT_BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY_DEPOSITS,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    results = requests.get(URL, params=params).json()
    # print("=== API 응답 데이터 ===2") # 출력 테스트용
    # print(params['auth'])
    # print(results)
    base_list = results['result']['baseList']
    option_list = results['result']['optionList']
    
    base_serializer = DepositProductsSerializerC(data=base_list, many=True)
    if base_serializer.is_valid():
        base_serializer.save()
    else:
        Response(base_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    for option in option_list:
        option_serializer = DepositOptionsSerializer(data=option)
        if option_serializer.is_valid():
            deposit_product = DepositProducts.objects.get(fin_prdt_cd=option['fin_prdt_cd'])
            option_serializer.save(fin_prdt_cd=deposit_product)
        else:
            Response(option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # option list 중복 제거
    duplicate_options = (
        DepositOptions.objects
        .values('fin_prdt_cd', 'save_trm')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
    )

    for duplicate in duplicate_options:
        fin_prdt_cd = duplicate['fin_prdt_cd']
        save_trm = duplicate['save_trm']
        duplicate_objects = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd, save_trm=save_trm)
        duplicate_objects.exclude(pk=duplicate_objects.first().pk).delete()

    return Response(base_serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def save_saving(request): # models에 저장하는 함수
    URL = DEPOSIT_BASE_URL + 'savingProductsSearch.json'
    params = {
        'auth': settings.API_KEY_DEPOSITS,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    results = requests.get(URL, params=params).json()
    # print("=== API 응답 데이터 ===2") # 출력 테스트용
    # print(params['auth'])
    # print(results)
    base_list = results['result']['baseList']
    option_list = results['result']['optionList']
    
    base_serializer = SavingProductsSerializerC(data=base_list, many=True)
    if base_serializer.is_valid():
        base_serializer.save()
    else:
        Response(base_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    for option in option_list:
        option_serializer = SavingOptionsSerializer(data=option)
        if option_serializer.is_valid():
            saving_product = SavingProducts.objects.get(fin_prdt_cd=option['fin_prdt_cd'])
            option_serializer.save(fin_prdt_cd=saving_product)
        else:
            Response(option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # option list 중복 제거
    duplicate_options = (
        SavingOptions.objects
        .values('fin_prdt_cd', 'save_trm')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
    )

    for duplicate in duplicate_options:
        fin_prdt_cd = duplicate['fin_prdt_cd']
        save_trm = duplicate['save_trm']
        duplicate_objects = SavingOptions.objects.filter(fin_prdt_cd=fin_prdt_cd, save_trm=save_trm)
        duplicate_objects.exclude(pk=duplicate_objects.first().pk).delete()

    return Response(base_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def summarize_product(request, product_id):
    try:
        product = DepositProducts.objects.get(pk=product_id)
    except DepositProducts.DoesNotExist:
        return Response({"error": "상품을 찾을 수 없습니다."}, status=404)

    summary = summarize_deposit_product(
        name=product.fin_prdt_nm,
        bank=product.kor_co_nm,
        etc_note=product.etc_note,
        spcl_cnd=product.spcl_cnd,
        join_member=product.join_member,
        join_way=product.join_way
    )

    return Response({
        "product_id": product_id,
        "summary": summary
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.recommend import recommend_products

@api_view(['POST'])
def gpt_recommendation(request):
    profile = {
        'age': request.data.get('age', ''),
        'asset': request.data.get('asset', ''),
        'goal': request.data.get('goal', ''),
        'type': request.data.get('type', '')
    }

    result = recommend_products(profile)
    return Response({"recommendation": result})


@api_view(['GET'])
def youtube_videos(request):
    query = request.GET.get("query", "금융")
    videos = search_youtube_videos(query)
    return Response({"results": videos})


@api_view(['GET'])
def get_gold_and_silver_prices(request):
    try:
        gold_data = fetch_gold_or_silver_data("XAU")
        silver_data = fetch_gold_or_silver_data("XAG")

        return Response({
            "XAU": gold_data,
            "XAG": silver_data
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['GET'])
def major_exchange_rates(request):
    try:
        data = get_major_exchange_rates()
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def convert_view(request):
    to = request.GET.get("to")
    amount = float(request.GET.get("amount", 1.0))
    try:
        result = convert_currency(to, amount)
        return Response({"converted": result})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def historical_exchange_rate(request):
    date = request.GET.get("date")
    symbols = request.GET.get("symbols", "KRW")
    try:
        data = get_historical_rate(date, symbols)
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def supported_currencies_view(request):
    try:
        data = get_supported_currencies()
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
