from django.shortcuts import render
from reservation.forms import ReservationForm

# Create your views here.
def home(request):
    context = {'form':ReservationForm()}
    return render(request, "home.html", context)

def menu(request):
    return render(request, "menu.html")

def book(request):
    context = {'form': ReservationForm()}
    return render(request, "book.html", context)

def about(request):
    return render(request, "about.html")
