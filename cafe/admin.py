from django.contrib import admin
from .models import FoodCategory, MenuItem, DailySpecial
# Register your models here.
class priceFilter(admin.SimpleListFilter):
    title = "Price"
    parameter_name = "price"

    def lookups(self, request, model_admin):
        return (
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        )

    def queryset(self, request, queryset):
        if self.value() == "low":
            return queryset.filter(price__lte=20)
        if self.value() == "medium":
            return queryset.filter(price__gte=20, price__lte=70)
        if self.value() == "high":
            return queryset.filter(price__gte=70)

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "image", "category", "slug", "created_at")
    list_editable = ("price","category",)
    list_filter = ("category", "created_at", priceFilter)
    search_fields = ["name__istartswith"]
    prepopulated_fields = {"slug": ["name"]}

class FoodCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name__istartswith"]
admin.site.register(FoodCategory,FoodCategoryAdmin)

admin.site.register(MenuItem,MenuItemAdmin)

class DailySpecialAdmin(admin.ModelAdmin):
    list_display = ("title", "food")
    list_editable = ("title","food")
    list_filter = ["title"]
    search_fields = ["title__istartswith"]
    list_display_links = None
    autocomplete_fields = ["food"]

admin.site.register(DailySpecial, DailySpecialAdmin)