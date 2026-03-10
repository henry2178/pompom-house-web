from django.db import models
from django.contrib.auth.models import AbstractUser

# User table
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    favorites = models.ManyToManyField('Property', blank=True, related_name='liked_by_users')

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        if full_name:
            return full_name

        return self.username

# Property table
class Property(models.Model):
    # filter student, only landlord can publish new property
    landlord = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name="Landlord",
        limit_choices_to={'is_landlord': True}
    )
    title = models.CharField(max_length=200, verbose_name="Property Name")
    address = models.CharField(max_length=255, verbose_name="Address")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price Per Week (£)")
    description = models.TextField(verbose_name="Description")
    photo = models.ImageField(upload_to='property_photos/', null=True, blank=True, verbose_name="Property Photo")
    created_time = models.DateTimeField(auto_now_add=True)
    bed_type = models.CharField(max_length=100, default="Double Bed", verbose_name="Bed Type")
    bathroom_type = models.CharField(max_length=100, default="En-suite", verbose_name="Bathroom Type")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="Rating")
    review_count = models.IntegerField(default=0, verbose_name="Review Count")
    favorites = models.ManyToManyField(User, related_name='favorite_properties', blank=True)

    def __str__(self):
        return self.title


# Booking table
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    weeks = models.PositiveIntegerField(verbose_name="Lease Duration (Weeks)")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price (£)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.tenant.username} -> {self.property.title} ({self.status})"


# Review table
class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} Stars for {self.property.title} by {self.student.username}"
