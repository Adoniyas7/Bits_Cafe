from django.shortcuts import render, redirect
from reservation.forms import ReservationForm
from django.contrib import messages
from django.core.mail import send_mail
from .models import FoodCategory, Review, Customer , MenuItem, DailySpecial, Cart, Order
from .forms import CustomerForm, ReviewForm, CustomerProfileForm 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    form = ReservationForm()
    # cart = Cart.objects.filter(user=request.user)
    # total_items = sum([item.quantity for item in cart])

    context = {"form": form,"categories": FoodCategory.objects.all(),
               'review_form': ReviewForm(),
               'reviews': Review.objects.all(),
               'menu_items': MenuItem.objects.all(),
               'daily_specials': DailySpecial.objects.all(),
            #    'total_items': total_items
               }
    if request.method =="POST":
        if 'reserve' in request.POST:
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
                return redirect("home")
        elif 'review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.save()
                messages.success(request, "Review Was Successful. Thank You For Your Feedback.")
                return redirect("home")
            else:
                messages.error(request, "Review Failed. Please Try Again")
                return redirect("home")
            
    return render(request, "home.html", context)

def menu(request):
    context = {"categories": FoodCategory.objects.all(),
               'menu_items': MenuItem.objects.all()}
    return render(request, "menu.html", context)

def book(request):
    context = {'form': ReservationForm()}
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
            return redirect("home")

    return render(request, "book.html", context)

def about(request):
    return render(request, "about.html")

def register(request):
    context = {'form': CustomerForm(), "page": "register"}
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration Successful. You Can Now Login.")
            return redirect("login") 
        else:
            print("error")
            print(form.errors)

            # messages.error(request, "Registration Failed. Please Try Again \n Ensure That Your Passwords Match" + str(form.errors))
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            return redirect("register")

    return render(request, "registration/register.html", context)

@login_required(login_url="login")
def profile(request):
    customer = Customer.objects.get_or_create(user=request.user)[0]
    context = {"form": CustomerProfileForm(instance=customer)}
    print(customer.user)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            request.user.first_name = customer.first_name
            request.user.last_name = customer.last_name
            request.user.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=customer)
        context = {"form": form, "customer": customer}
    return render(request, 'registration/profile.html', context)

@login_required(login_url="login")
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = sum([item.item.price * item.quantity for item in cart])
    total_items = sum([item.quantity for item in cart])
    context = {"cart_items": cart,
               "total_items": total_items,
               "total_price": total_price,
               }
    return render(request, "cart.html", context)

@login_required(login_url="login")
def add_to_cart(request, id):
    item = MenuItem.objects.get(id=id)
    if Cart.objects.filter(user=request.user, item=item).exists():
        cart_item = Cart.objects.filter(user=request.user).get(item = item)
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            user=request.user,
            item=item,
            quantity=1)

    return redirect("cart")

@login_required(login_url="login")
def remove_from_cart(request, id):
    item = Cart.objects.filter(user=request.user).get(id=id)
    item.delete()
    return redirect("cart")

@login_required(login_url="login")
def update_cart(request, id):
    item = Cart.objects.filter(user=request.user).get(id=id)
    quantity = request.POST.get("quantity")
    item.quantity = quantity
    item.save()

    # total = float(item.item.price) * int(quantity)
    # print(total)
    return redirect("cart")

@login_required(login_url="login")
def order(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = sum([item.item.price * item.quantity for item in cart])
    order = Order(
        user=request.user,
        total=total_price,
    )
    order.save()
    order.items.set(cart)
    print("Order created")

    context = {"cart_items": cart,
               "item_count": cart.count(),
               "total_price": total_price,
               }
    messages.success(request, "Order placed successfully. Thank you for ordering.")
    return render(request, "order.html", context)
