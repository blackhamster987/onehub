from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.email


class Hotel(models.Model):
    CATEGORY_CHOICES = [
        ('family', 'Family'),
        ('bachelor', 'Bachelor'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    hotelowner = models.CharField(max_length=100)
    hotelname = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='family')
    price_per_night = models.PositiveIntegerField(default=0)
    total_rooms = models.PositiveIntegerField(default=0)
    available_rooms = models.PositiveIntegerField(default=0)

    @property
    def average_rating(self):
        from django.db.models import Avg
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return avg if avg is not None else 0

    def __str__(self):
        return f"{self.hotelowner} ({self.status})"


class HotelRating(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hotel_ratings'
    )
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hotel', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.hotel.hotelowner}: {self.rating}"


class Room(models.Model):
    CATEGORY_CHOICES = [
        ('family', 'Family'),
        ('bachelor', 'Bachelor'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    ]

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    price_per_night = models.PositiveIntegerField()
    total_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()

    image = models.ImageField(
        upload_to='room_images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.hotel.hotelowner} - {self.category}"


class HotelBooking(models.Model):
    """Hotel room booking with approval workflow"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    check_in = models.DateField()
    check_out = models.DateField()
    rooms_booked = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.hotel.hotelowner} ({self.status})"


# ================= ECOMMERCE MODELS =================

class EcommerceAdmin(models.Model):
    """Model for ecommerce admin users"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # Will store hashed password
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.status})"

    class Meta:
        verbose_name = "Ecommerce Admin"
        verbose_name_plural = "Ecommerce Admins"


class Product(models.Model):
    """Model for grocery products"""
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('footwear', 'Footwear'),
        ('accessories', 'Accessories'),
        ('books', 'Books'),
        ('stationery', 'Stationery'),
    ]

    ecommerce_admin = models.ForeignKey(
        EcommerceAdmin,
        on_delete=models.CASCADE,
        related_name='products'
    )
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    total_quantity = models.IntegerField()
    availability_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} ({self.ecommerce_admin.full_name})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"



class EcommerceOrder(models.Model):
    """Model for ecommerce orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ecommerce_orders'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    quantity = models.PositiveIntegerField(default=1)
    
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
    ]
    payment_method = models.CharField(
        max_length=10, 
        choices=PAYMENT_CHOICES, 
        default='cod'
    )
    upi_id = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.product_name} ({self.status})"

    class Meta:
        ordering = ['-created_at']


# ================= TOURIST PLACES MODELS =================

class TouristPlace(models.Model):
    """Tourist places model with essential fields"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    opening_time = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 9:00 AM - 6:00 PM")
    location_link = models.URLField(max_length=500, blank=True, null=True, help_text="Google Maps URL or location link")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tourist Place"
        verbose_name_plural = "Tourist Places"

    def __str__(self):
        return self.name


class TouristPlaceImage(models.Model):
    """Images for tourist places"""
    tourist_place = models.ForeignKey(
        TouristPlace,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='tourist_places/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Tourist Place Image"
        verbose_name_plural = "Tourist Place Images"

    def __str__(self):
        return f"Image for {self.tourist_place.name}"
