from django.urls import path, include
from . import views
import reservation.views as rviews
import django.contrib.auth.views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("book/", rviews.book_table, name="book"),
    path("book/cancel/<int:id>/", rviews.cancel_reservation, name="cancel_reservation"),
    path("book/cancel/", rviews.cancel_reservation_success, name="cancel_reservation_success"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("", include("django.contrib.auth.urls")),
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="rest_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("profile/", views.profile, name="profile"),
    path("cart/", views.cart, name="cart"),

]