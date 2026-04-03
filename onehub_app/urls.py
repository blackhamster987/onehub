from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # User
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('profile/', views.profile, name='profile'),
    path('chatbot/', views.chatbot, name='chatbot'),

 
    
    # Online Store
    path('store/', views.online_store, name='online_store'),
    path('store/buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('store/bookings/', views.online_bookings, name='online_bookings'),
    path('store/order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    

    # Hotel Booking System (User)
    path('hotels/book/', views.hotel_bookings, name='hotel_bookings'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('hotels/review/<int:hotel_id>/', views.submit_hotel_review, name='submit_hotel_review'),

    # Hotel Admin
    path('hotel-admin/register/', views.hotel_admin_register, name='hotel_admin_register'),
    path('hotel-admin/login/', views.hotel_admin_login, name='hotel_admin_login'),
    path('hotel-admin/dashboard/', views.hotel_admin_dashboard, name='hotel_admin_dashboard'),
    path('hotel-admin/logout/', views.hotel_admin_logout, name='hotel_admin_logout'),
    
    # Hotel Admin - Booking Management
    path('hotel-admin/bookings/', views.hotel_admin_bookings, name='hotel_admin_bookings'),
    path('hotel-admin/booking/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('hotel-admin/booking/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),

    # Rooms
    path('hotel-admin/add-room/<int:hotel_id>/', views.add_room_type, name='add_room_type'),
    path('room/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('room/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    path('hotel/<int:hotel_id>/delete/', views.delete_hotel, name='delete_hotel'),
    path('room/<int:room_id>/upload-image/', views.upload_room_image, name='upload_room_image'),

    # ===== ONEHUB CUSTOM ADMIN =====
    # Login & Dashboard
    path('onehub-admin/login/', views.onehub_admin_login, name='onehub_admin_login'),
    path('onehub-admin/dashboard/', views.onehub_admin_dashboard, name='onehub_admin_dashboard'),
    path('onehub-admin/logout/', views.onehub_admin_logout, name='onehub_admin_logout'),
    
    # Hotel Owner Management
    path('onehub-admin/hotel-owners/', views.hotel_owners_list, name='hotel_owners_list'),
    path('onehub-admin/hotel/approve/<int:id>/', views.approve_hotel_owner, name='approve_hotel_owner'),
    path('onehub-admin/hotel/reject/<int:id>/', views.reject_hotel_owner, name='reject_hotel_owner'),
    path('onehub-admin/hotel/delete/<int:id>/', views.delete_hotel_owner, name='delete_hotel_owner'),

    
    # Ecommerce Owner Management
    path('onehub-admin/ecommerce-owners/', views.ecommerce_owners_list, name='ecommerce_owners_list'),
    path('onehub-admin/ecommerce/approve/<int:id>/', views.approve_ecommerce_owner, name='approve_ecommerce_owner'),
    path('onehub-admin/ecommerce/reject/<int:id>/', views.reject_ecommerce_owner, name='reject_ecommerce_owner'),
    path('onehub-admin/ecommerce/delete/<int:id>/', views.delete_ecommerce_owner, name='delete_ecommerce_owner'),

    # User Management
    path('onehub-admin/users/', views.users_list, name='users_list'),
    path('onehub-admin/user/delete/<int:id>/', views.delete_user, name='delete_user'),

    # Legacy admin URLs (for backwards compatibility)
    path('admin/hotel-requests/', views.super_admin_hotels, name='super_admin_hotels'),
    path('admin/approve-hotel/<int:hotel_id>/', views.approve_hotel, name='approve_hotel'),
    path('admin/reject-hotel/<int:hotel_id>/', views.reject_hotel, name='reject_hotel'),

    # ===== ECOMMERCE ADMIN =====
    path('ecommerce/register/', views.ecommerce_register, name='ecommerce_register'),
    path('ecommerce/login/', views.ecommerce_login, name='ecommerce_login'),
    path('ecommerce/logout/', views.ecommerce_logout, name='ecommerce_logout'),
    path('ecommerce/dashboard/', views.ecommerce_dashboard, name='ecommerce_dashboard'),
    path('ecommerce/product/add/', views.ecommerce_add_product, name='ecommerce_add_product'),
    path('ecommerce/product/edit/<int:id>/', views.ecommerce_edit_product, name='ecommerce_edit_product'),
    path('ecommerce/product/delete/<int:id>/', views.ecommerce_delete_product, name='ecommerce_delete_product'),
    path('ecommerce/orders/', views.ecommerce_orders, name='ecommerce_orders'),
    path('ecommerce/order/update/<int:order_id>/', views.ecommerce_update_order_status, name='ecommerce_update_order_status'),

    # ===== TOURIST PLACES =====
    path('onehub-admin/tourist-places/', views.tourist_places_list, name='tourist_places_list'),
    path('onehub-admin/tourist-places/add/', views.add_tourist_place, name='add_tourist_place'),
    path('onehub-admin/tourist-places/edit/<int:id>/', views.edit_tourist_place, name='edit_tourist_place'),
    path('onehub-admin/tourist-places/delete/<int:id>/', views.delete_tourist_place, name='delete_tourist_place'),
    path('onehub-admin/tourist-places/delete-image/<int:image_id>/', views.delete_tourist_image, name='delete_tourist_image'),

    # User-facing tourist places
    path('destinations/', views.tourist_places, name='tourist_places'),

]

