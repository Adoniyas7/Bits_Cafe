from django.contrib import admin
from .models import FoodCategory, MenuItem, DailySpecial, Customer, Review, Cart, Order
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

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "review", "date_created", "approved")
    list_editable = ("approved",)
    list_filter = ["approved"]
    autocomplete_fields = ["user"]

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "email", "phone_number", "profile_pic", "created_at")
    list_filter = ["created_at"]
    search_fields = ["first_name__istartswith", "last_name__istartswith", "email__istartswith"]
    autocomplete_fields = ["user"]
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "items_list", "total", "status", "created_at")
    list_filter = ["status", "created_at"]
    list_editable = ("status",)
    search_fields = ["user__istartswith"]
    autocomplete_fields = ["user"]

    def items_list(self, obj):
        return "\n, ".join([p.item.name for p in obj.items.all()])

admin.site.register(DailySpecial, DailySpecialAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
