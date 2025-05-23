from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer,UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomLoginSerializer(LoginSerializer):
    # email 필드 제거
    email = None

class CustomRegisterSerializer(RegisterSerializer):
    # 기본 필드(username, password1, password2) + 커스텀 필드 추가
    nickname = serializers.CharField(required=True, max_length=20)
    name = serializers.CharField(required=True, max_length=20)
    phonenumber = serializers.CharField(required=False, max_length=11, allow_blank=True)
    age = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True, max_length=20)
    gender = serializers.IntegerField(required=True)
    salary = serializers.IntegerField(required=True)
    wealth = serializers.IntegerField(required=True)

    # 필수: 추가 필드 정의
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'nickname': self.validated_data.get('nickname', ''),
            'name': self.validated_data.get('name', ''),
            'phonenumber': self.validated_data.get('phonenumber', ''),
            'age': self.validated_data.get('age', 20),
            'email': self.validated_data.get('email', ''),
            'gender': self.validated_data.get('gender', 0),
            'salary': self.validated_data.get('salary', 0),
            'wealth': self.validated_data.get('wealth', 0),
        })
        return data

    # 필수: 유저 생성 로직 오버라이드
    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname')
        user.name = self.validated_data.get('name')
        user.phonenumber = self.validated_data.get('phonenumber')
        user.age = self.validated_data.get('age')
        user.email = self.validated_data.get('email')
        user.gender = self.validated_data.get('gender')
        user.salary = self.validated_data.get('salary')
        user.wealth = self.validated_data.get('wealth')
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk','username', 'nickname', 'name', 'phonenumber', 'age', 'email', 'gender','salary', 'wealth', 'deposit', 'saving']

class CustomUserDetailsSerializer(UserDetailsSerializer):
    nickname = serializers.CharField(required=True, max_length=20)
    name = serializers.CharField(required=True, max_length=20)
    phonenumber = serializers.CharField(required=False, max_length=11, allow_blank=True)
    age = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True, max_length=20)
    gender = serializers.IntegerField(required=True)
    salary = serializers.IntegerField(required=True)
    wealth = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = (
            'pk', 'username', 'nickname', 'name', 'phonenumber', 'age', 'email',
            'gender', 'salary', 'wealth'
        )
        read_only_fields = ('username',)  # username을 read-only로 지정

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.name = validated_data.get('name', instance.name)
        instance.phonenumber = validated_data.get('phonenumber', instance.phonenumber)
        instance.age = validated_data.get('age', instance.age)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.wealth = validated_data.get('wealth', instance.wealth)
        instance.save()
        return instance