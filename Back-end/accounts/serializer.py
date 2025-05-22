from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True, allow_blank=False)
    name = serializers.CharField(required=True, allow_blank=False)
    phonenumber = serializers.IntegerField(required=False, allow_null=False)
    age = serializers.IntegerField(required=True, allow_null=False)
    email = serializers.CharField(required=True, allow_blank=False)
    gender = serializers.IntegerField(required=True, allow_blank=False)
    salary = serializers.IntegerField(required=True, allow_null=False)
    wealth = serializers.IntegerField(required=True, allow_null=False)
   

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()

        data_dict['nickname'] = self.validated_data.get('nickname', None)
        data_dict['name'] = self.validated_data.get('name', None)
        data_dict['phonenumber'] = self.validated_data.get('phonenumber', None)
        data_dict['age'] = self.validated_data.get('age', None)
        data_dict['email'] = self.validated_data.get('email', None)
        data_dict['gender'] = self.validated_data.get('email', None)
        data_dict['salary'] = self.validated_data.get('email', None)
        data_dict['wealth'] = self.validated_data.get('wealth', None)
        
        return data_dict
    
    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname', None)
        user.name = self.validated_data.get('name', None)
        user.phonenumber = self.validated_data.get('phonenumber', None)
        user.age = self.validated_data.get('age', None)
        user.email = self.validated_data.get('email', None)
        user.gender = self.validated_data.get('gender', None)
        user.salary = self.validated_data.get('salary', None)
        user.wealth = self.validated_data.get('wealth', None)
        user.save()
        return user
    