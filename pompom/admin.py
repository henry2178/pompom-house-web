from django.contrib import admin
from .models import User, Property, Booking, Review

# register
admin.site.register(User)
admin.site.register(Property)
admin.site.register(Booking)
admin.site.register(Review)