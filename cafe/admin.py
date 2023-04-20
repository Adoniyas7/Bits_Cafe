from django.contrib import admin
from .models import FoodCategory, MenuItem
# Register your models here.
class FoodCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name__istartswith"]
admin.site.register(FoodCategory,FoodCategoryAdmin)

admin.site.register(MenuItem)

