from django.conf import settings
from rest_framework.response import Response
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts
from .serializers import DepositProductsSerializerD, DepositProductsSerializerC, DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializerD, SavingProductsSerializerC, SavingProductsSerializer, SavingOptionsSerializer
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from django.shortcuts import get_object_or_404
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
def summarize_product(request, product_fin_prdt_cd):
    product = None
    # 1. DepositProducts에서 먼저 찾기
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=product_fin_prdt_cd)
    except DepositProducts.DoesNotExist:
        pass

    # 2. 없으면 SavingProducts에서 찾기
    if not product:
        try:
            product = SavingProducts.objects.get(fin_prdt_cd=product_fin_prdt_cd)
        except SavingProducts.DoesNotExist:
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
        "product_fin_prdt_cd": product_fin_prdt_cd,
        "summary": summary
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.recommend import recommend_products

from dataclasses import dataclass
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DepositOptions, SavingOptions


@dataclass
class UserProfile:
    age: str
    asset: str
    goal: str
    type: str  # 예금 or 적금


def filter_options(profile, options):
    filtered = options

    if profile.age in ['10대', '20대']:
        filtered = [opt for opt in filtered if opt['save_trm'] <= 12]
    elif profile.age in ['30대', '40대']:
        filtered = [opt for opt in filtered if 12 <= opt['save_trm'] <= 24]
    elif profile.age in ['50대', '60대 이상']:
        filtered = [opt for opt in filtered if opt['save_trm'] >= 24]

    if profile.goal == '생활비':
        filtered = [opt for opt in filtered if opt['save_trm'] <= 12]
    elif profile.goal == '주택':
        filtered = [opt for opt in filtered if opt['save_trm'] >= 24]
    elif profile.goal == '노후 준비':
        filtered = [opt for opt in filtered if opt['intr_rate2'] >= 3.0]

    if profile.asset in ['~300만', '~500만']:
        filtered = [opt for opt in filtered if opt['intr_rate2'] >= 2.0]
    elif profile.asset == '1억 이상':
        filtered = [opt for opt in filtered if opt['intr_rate2'] >= 3.5]

    return filtered


def get_top_recommendations(filtered_options, limit=3):
    seen = set()
    result = []
    for opt in sorted(filtered_options, key=lambda x: x['intr_rate2'], reverse=True):
        if opt['fin_prdt_nm'] not in seen:
            result.append(opt)
            seen.add(opt['fin_prdt_nm'])
        if len(result) == limit:
            break
    return result


@api_view(['POST'])
def gpt_recommendation(request):
    profile = UserProfile(
        age=request.data.get('age', ''),
        asset=request.data.get('asset', ''),
        goal=request.data.get('goal', ''),
        type=request.data.get('type', '')
    )

    raw_data = []

    if profile.type == '예금':
        options = DepositOptions.objects.select_related('fin_prdt_cd').all()
        for opt in options:
            raw_data.append({
                "fin_prdt_cd": opt.fin_prdt_cd.fin_prdt_cd,  # ✅ 추가
                "fin_prdt_nm": opt.fin_prdt_cd.fin_prdt_nm,
                "kor_co_nm": opt.fin_prdt_cd.kor_co_nm,
                "save_trm": opt.save_trm,
                "intr_rate2": opt.intr_rate2,
                "etc_note": opt.fin_prdt_cd.etc_note,
                "spcl_cnd": opt.fin_prdt_cd.spcl_cnd,
                "join_way": opt.fin_prdt_cd.join_way
            })
    else:
        options = SavingOptions.objects.select_related('fin_prdt_cd').all()
        for opt in options:
            raw_data.append({
                "fin_prdt_cd": opt.fin_prdt_cd.fin_prdt_cd,  # ✅ 추가
                "fin_prdt_nm": opt.fin_prdt_cd.fin_prdt_nm,
                "kor_co_nm": opt.fin_prdt_cd.kor_co_nm,
                "save_trm": opt.save_trm,
                "intr_rate2": opt.intr_rate2,
                "etc_note": opt.fin_prdt_cd.etc_note,
                "spcl_cnd": opt.fin_prdt_cd.spcl_cnd,
                "join_way": opt.fin_prdt_cd.join_way
            })

    filtered = filter_options(profile, raw_data)
    recommendations = get_top_recommendations(filtered, limit=3)

    return Response({"recommendation": recommendations})

@api_view(['GET'])
def youtube_videos(request):
    user_query = request.GET.get("query", "")  # 사용자가 입력한 키워드
    base_query = "금융"

    # 🔍 사용자가 입력하면 붙이고, 아니면 금융만
    final_query = f"{user_query} {base_query}".strip()

    videos = search_youtube_videos(final_query)
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









@api_view(['GET'])
def product_detail(request, product_type, fin_prdt_cd):
    """
    상품 상세 정보와 해당 옵션들을 함께 반환하는 API
    """
    try:
        if product_type == 'deposit':
            # 예금 상품 정보 가져오기
            product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
            product_serializer = DepositProductsSerializer(product)
            
            # 해당 예금의 옵션들 가져오기
            options = DepositOptions.objects.filter(fin_prdt_cd=product)
            options_serializer = DepositOptionsSerializer(options, many=True)
            
        elif product_type == 'saving':
            # 적금 상품 정보 가져오기
            product = get_object_or_404(SavingProducts, fin_prdt_cd=fin_prdt_cd)
            product_serializer = SavingProductsSerializer(product)
            
            # 해당 적금의 옵션들 가져오기
            options = SavingOptions.objects.filter(fin_prdt_cd=product)
            options_serializer = SavingOptionsSerializer(options, many=True)
            
        else:
            return Response(
                {'error': 'Invalid product type. Use "deposit" or "saving"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 상품 정보와 옵션 정보를 함께 반환
        response_data = {
            'product': product_serializer.data,
            'options': options_serializer.data,
            'product_type': product_type
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def deposit_list(request):
    """예금 상품 목록 반환"""
    deposits = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saving_list(request):
    """적금 상품 목록 반환"""
    savings = SavingProducts.objects.all()
    serializer = SavingProductsSerializer(savings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_options_list(request):
    """예금 옵션 목록 반환"""
    options = DepositOptions.objects.all()
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saving_options_list(request):
    """적금 옵션 목록 반환"""
    options = SavingOptions.objects.all()
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)
