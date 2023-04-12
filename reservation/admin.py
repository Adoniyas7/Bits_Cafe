from django.contrib import admin
from .models import Reservation

# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "event", "people", "date", "time", "status", "created_at")
    list_editable = ["status"]
    list_filter = ["status", "created_at"]
    list_per_page=10

admin.site.register(Reservation, ReservationAdmin)
