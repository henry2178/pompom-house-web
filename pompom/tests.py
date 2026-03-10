from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Property, Booking

User = get_user_model()

class PompomHouseTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.landlord = User.objects.create_user(
            username='test_landlord',
            password='testpassword123',
            email='landlord@test.ac.uk'
        )
        self.landlord.is_landlord = True
        self.landlord.save()

        self.property = Property.objects.create(
            landlord=self.landlord,
            title="Vita Student West End",
            address="123 Test St, Glasgow",
            price=250.00,
            description="Best accommodation!",
            rating=5.0,
            review_count=10
        )

    def test_property_creation(self):
        prop = Property.objects.get(id=self.property.id)
        self.assertEqual(prop.title, "Vita Student West End")
        self.assertEqual(prop.landlord.username, "test_landlord")

    def test_home_page_loads_correctly(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vita Student West End")

    def test_landlord_dashboard_access_denied_for_anonymous(self):
        response = self.client.get(reverse('landlord_dashboard'))
        self.assertEqual(response.status_code, 302)