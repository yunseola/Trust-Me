from django.conf import settings
from rest_framework.response import Response
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts
from .serializers import DepositProductsSerializerD, DepositProductsSerializerC, DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializerD, SavingProductsSerializerC, SavingProductsSerializer, SavingOptionsSerializer
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from deposits.models import DepositProducts
from .services.summary import summarize_deposit_product

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