from django.urls import path, include
from . import views
import reservation.views as rviews

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("book/", rviews.book_table, name="book"),
    path("book/cancel/<int:id>/", rviews.cancel_reservation, name="cancel_reservation"),
    path("book/cancel/", rviews.cancel_reservation_success, name="cancel_reservation_success"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("", include("django.contrib.auth.urls")),


]