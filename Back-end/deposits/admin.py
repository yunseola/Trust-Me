from django.contrib import admin
from .models import DepositProducts
from .models import SavingProducts
# Register your models here.
admin.site.register(DepositProducts)
admin.site.register(SavingProducts)