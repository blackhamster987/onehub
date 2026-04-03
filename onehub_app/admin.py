from django.contrib import admin
from .models import User, Hotel, Room, HotelBooking, EcommerceAdmin, Product


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'phone', 'age']
    search_fields = ['email', 'name']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['hotelowner', 'email', 'location', 'status', 'total_rooms']
    list_filter = ['status', 'category']
    search_fields = ['hotelowner', 'email', 'location']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'category', 'price_per_night', 'total_rooms', 'available_rooms']
    list_filter = ['category']
    search_fields = ['hotel__hotelowner']


@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'room', 'check_in', 'check_out', 'rooms_booked', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'hotel__hotelowner']


@admin.register(EcommerceAdmin)
class EcommerceAdminAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'created_at']
    search_fields = ['full_name', 'email']
    readonly_fields = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'price', 'total_quantity', 
                    'availability_status', 'created_at']
    list_filter = ['category', 'availability_status', 'created_at']
    search_fields = ['product_name', 'description']
    readonly_fields = ['created_at', 'updated_at']





# Register your models here.

