from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel, DealerReview
from .restapis import get_request, get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Static view
def static_view(request):
    return render(request, 'djangoapp/static.html')

# Get an instance of a logger
logger = logging.getLogger(__name__)

# About view to render static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Contact view to render static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Login view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Logout view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Registration view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    if request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, 
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Dealerships view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/ad39ee7e-0d06-4e9e-8de9-35be2c866619/actions/dealership-package/get_dealerships"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Dealer details view to render the reviews of a dealer
def get_dealer_details(request):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/ad39ee7e-0d06-4e9e-8de9-35be2c866619/actions/dealership-package/get_dealerships"
        dealer = get_dealers_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
                      
        review_url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/ad39ee7e-0d06-4e9e-8de9-35be2c866619/actions/dealership-package/get_reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
# def add_review(request, dealer_id):
#     if request.method == "POST":
#         context = {}
#         dealer_url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/ad39ee7e-0d06-4e9e-8de9-35be2c866619/actions/dealership-package/get_dealerships"
#         dealer = get_dealer_from_cf_by_id(dealer_url, id=dealer_id)
#         context["dealer"] = dealer
#     
#         review_url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/ad39ee7e-0d06-4e9e-8de9-35be2c866619/actions/dealership-package/get_reviews"
#         reviews = get_dealer_reviews_from_cf(review_url, id=dealer_id)
#         print(reviews)
#         context["reviews"] = reviews
#         
#         return render(request, 'djangoapp/add_review.html', context)
