from django.db import models
from django.utils.timezone import now
from django.core import serializers
import uuid
import json

# Car Make model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100, default='Make')
    description = models.CharField(max_length=500)

    def __str__(self):
        return "Name: " + self.name

# Car Model model
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    name = models.CharField(null=False, max_length=40, default='undefined')
    # - Name
    id = models.IntegerField(default=1, primary_key=True)      
    # - Dealer id, used to refer a dealer created in cloudant database
    
    COUPE = 'Coupe'
    MINIVAN = 'Minivan'
    SEDAN = 'Sedan'
    SUV = 'SUV'
    TRUCK = 'Truck'
    WAGON = 'Wagon'
    CAR_TYPES = [
        (COUPE, 'Coupe'),
        (MINIVAN, 'Minivan'),
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (TRUCK, 'Truck'),
        (WAGON, 'Wagon'),
    ]

    type = models.CharField(
        null=False,
        max_length=50,
        choices=CAR_TYPES,
        default=SEDAN
    )
        
    year = models.IntegerField(default=now().year)

    def __str__(self):
        return "Name: " + self.name

# Get dealer data
class CarDealer:

    def __init__(self, address, city, id, lat, long, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
       
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long

        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer Name: " + self.full_name

# Get review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # Optional attributes
        self.purchase_date = ""
        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)

# Post review data
class ReviewPost:

    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)