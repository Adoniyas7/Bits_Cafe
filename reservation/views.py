from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.contrib import messages
from django.core.mail import send_mail
from .models import Reservation

# Create your views here.
def book_table(request):
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
            email_from = 'bitzcaffe@gmail.com'
            email_to = reservation.email
            print(message, email_to, email_from)
            send_mail(subject, message, email_from, [email_to])
            #--------------------------------------------

            return redirect("book")
        else:
            messages.error(request, "Reservation Failed. Please Try Again")
    return render(request, "book.html", context)

def cancel_reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    if request.method == "POST":
        print("POST")
        reservation.delete()
        messages.success(request, "Reservation Cancelled Successfully")
        return redirect("cancel_reservation_success")
    return render(request, "cancel_booking.html", {"reservation": reservation})

def cancel_reservation_success(request):
    return render(request, "cancel_booking_success.html")