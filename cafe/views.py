from django.shortcuts import render, redirect
from reservation.forms import ReservationForm
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
def home(request):
    form = ReservationForm()
    context = {"form": form}
    if request.method =="POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            form = ReservationForm()
            messages.success(request, "Reservation Was Successful. Check Your Email For Confirmation.")
            #sending email
            #--------------------------------------------
            subject = "Reservation Confirmation"
            message = f"Hello {reservation.name}, \n\nThank you for making a reservation with us. \n\nYour reservation details are as follows: \n\nEvent: {reservation.event} \nDate: {reservation.date} \nTime: {reservation.time} \nNumber of People: {reservation.people} \n\nWe look forward to seeing you. \n\nRegards, \nto cancel your reservation, click on the link below \n\nhttp://127.0.0.1:8000/book/cancel/{reservation.id} \n\n Regards, \nBits Cafe"
            email_from = 'adoniyasg7s@gmail.com'
            email_to = reservation.email
            print(message, email_to, email_from)
            send_mail(subject, message, email_from, [email_to])
            #--------------------------------------------

            return redirect("home")
        else:
            messages.error(request, "Reservation Failed. Please Try Again")
    return render(request, "home.html", context)
    # context = {'form':ReservationForm()}
    # return render(request, "home.html", context)

def menu(request):
    return render(request, "menu.html")

def book(request):
    context = {'form': ReservationForm()}
    return render(request, "book.html", context)

def about(request):
    return render(request, "about.html")
