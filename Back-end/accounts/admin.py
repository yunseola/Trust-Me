from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'age','email', 'gender', 'salary', 'wealth')
    fields = ('username', 'password','email', 'age', 'gender', 'salary', 'wealth')
    
admin.site.register(User,UserAdmin)