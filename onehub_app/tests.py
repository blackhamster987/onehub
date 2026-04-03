from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Hotel, HotelRating

class HotelRatingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='user@example.com', password='password')
        self.hotel = Hotel.objects.create(
            hotelowner='Test Hotel Owner',
            location='Test Location',
            email='test@hotel.com',
            password='password',
            status='approved'
        )

    def test_rating_submission(self):
        # Login user via session
        session = self.client.session
        session['email'] = 'user@example.com'
        session.save()

        response = self.client.post(reverse('submit_hotel_review', kwargs={'hotel_id': self.hotel.id}), {
            'rating': 4,
            'comment': 'Good stay'
        })
        self.assertRedirects(response, reverse('hotel_bookings'))
        
        # Verify rating created
        rating = HotelRating.objects.get(user=self.user, hotel=self.hotel)
        self.assertEqual(rating.rating, 4)
        self.assertEqual(rating.comment, 'Good stay')

    def test_average_rating_calculation(self):
        # Create another user and rating
        user2 = User.objects.create(email='user2@example.com', password='password')
        HotelRating.objects.create(user=self.user, hotel=self.hotel, rating=5)
        HotelRating.objects.create(user=user2, hotel=self.hotel, rating=3)

        # Average should be 4.0
        self.assertEqual(self.hotel.average_rating, 4.0)
