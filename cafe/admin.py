from django.contrib import admin
from .models import FoodCategory
# Register your models here.
class FoodCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name__istartswith"]
admin.site.register(FoodCategory,FoodCategoryAdmin)

