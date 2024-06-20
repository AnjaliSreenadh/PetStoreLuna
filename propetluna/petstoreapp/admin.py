
from django.contrib import admin
from .models import *
class ProductAdmin(admin.ModelAdmin):
  list_display=['id','pname','pcost','pdetails','cat','is_active']

admin.site.register(Product)
# admin.site.register(Cart)
# Register your models here.
from django.contrib import admin

# Register your models here.
