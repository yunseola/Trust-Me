from rest_framework import serializers
from .models import DepositProducts, DepositOptions, SavingOptions, SavingProducts
from django.db.models import Max

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)

class DepositProductsSerializer(serializers.ModelSerializer):
    DepositOptions.fin_prdt_cd_set = DepositOptionsSerializer(many=True)
    
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositProductsSerializerC(serializers.ModelSerializer):
    DepositOptions.fin_prdt_cd_set = DepositOptionsSerializer(many=True)
    user_count = serializers.SerializerMethodField()
    max_intr = serializers.SerializerMethodField()

    def get_user_count(self, obj):
        temp = DepositProducts.objects.get(fin_prdt_cd=obj['fin_prdt_cd'])
        return temp.joined.count()
    
    def get_max_intr(self, obj):
        temps = DepositOptions.objects.filter(fin_prdt_cd=DepositProducts.objects.get(fin_prdt_cd=obj['fin_prdt_cd']).pk)
        max_intr = temps.aggregate(max_intr=Max('intr_rate2'))['max_intr']
        return max_intr
    
    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositProductsSerializerD(serializers.ModelSerializer):
    DepositOptions.fin_prdt_cd_set = DepositOptionsSerializer(many=True)
    user_count = serializers.SerializerMethodField()
    max_intr = serializers.SerializerMethodField()

    def get_user_count(self, obj):
        return obj.joined.count()
    
    def get_max_intr(self, obj):
        temps = DepositOptions.objects.filter(fin_prdt_cd=obj.pk)
        max_intr = temps.aggregate(max_intr=Max('intr_rate2'))['max_intr']
        return max_intr
    
    class Meta:
        model = DepositProducts
        fields = '__all__'


class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)

class SavingProductsSerializer(serializers.ModelSerializer):
    SavingOptions.fin_prdt_cd_set = SavingOptionsSerializer(many=True)
    
    class Meta:
        model = SavingProducts
        fields = '__all__'

class SavingProductsSerializerC(serializers.ModelSerializer):
    SavingOptions.fin_prdt_cd_set = SavingOptionsSerializer(many=True)
    user_count = serializers.SerializerMethodField()
    max_intr = serializers.SerializerMethodField()

    def get_user_count(self, obj):
        temp = SavingProducts.objects.get(fin_prdt_cd=obj['fin_prdt_cd'])
        return temp.joined2.count()
    
    def get_max_intr(self, obj):
        temps = SavingOptions.objects.filter(fin_prdt_cd=SavingProducts.objects.get(fin_prdt_cd=obj['fin_prdt_cd']).pk)
        max_intr = temps.aggregate(max_intr=Max('intr_rate2'))['max_intr']
        return max_intr
    
    class Meta:
        model = SavingProducts
        fields = '__all__'


class SavingProductsSerializerD(serializers.ModelSerializer):
    SavingOptions.fin_prdt_cd_set = SavingOptionsSerializer(many=True)
    user_count = serializers.SerializerMethodField()
    max_intr = serializers.SerializerMethodField()

    def get_user_count(self, obj):
        return obj.joined.count()
    
    def get_max_intr(self, obj):
        temps = SavingOptions.objects.filter(fin_prdt_cd=obj.pk)
        max_intr = temps.aggregate(max_intr=Max('intr_rate2'))['max_intr']
        return max_intr
    
    class Meta:
        model = SavingProducts
        fields = '__all__'