from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Hotel, User, Room, HotelBooking, HotelRating
from .services import (
    FoodDeliveryService, CabBookingService, FlightBookingService,
    TrainBookingService, HotelBookingService, FuelDeliveryService
)
from .chatbot import OneHubChatbot
import json
import requests
from datetime import datetime
from django.conf import settings


# ================= GENERAL =================

def index(request):
    return render(request, 'index.html')


# ================= USER =================

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email exists');window.location='/register/'</script>")

        User.objects.create(
            name=request.POST.get('name'),
            age=request.POST.get('age'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            email=email,
            password=request.POST.get('password'),
            gender=request.POST.get('gender'),
            image=request.FILES.get('image')
        )
        return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        try:
            User.objects.get(
                email=request.POST.get('email'),
                password=request.POST.get('password')
            )
            request.session['email'] = request.POST.get('email')
            return redirect('userdashboard')
        except User.DoesNotExist:
            return HttpResponse("<script>alert('Invalid login');window.location='/login/'</script>")
    return render(request, 'login.html')


def userdashboard(request):
    if 'email' not in request.session:
        return redirect('login')
    return render(request, 'userdashboard.html')


def logout(request):
    request.session.flush()
    return redirect('index')


def profile(request):
    """User profile page"""
    if 'email' not in request.session:
        return redirect('login')
    
    user = User.objects.get(email=request.session['email'])
    
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.age = request.POST.get('age')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.gender = request.POST.get('gender')
        user.address = request.POST.get('address')
        
        if request.FILES.get('image'):
            user.image = request.FILES.get('image')
            
        user.save()
        request.session['email'] = user.email
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
        
    return render(request, 'profile.html', {'user': user})


# ================= SERVICE PAGES =================

def food(request):
    """Food delivery service page"""
    if 'email' not in request.session:
        return redirect('login')
    return render(request, 'services/food.html')


def cab(request):
    """Cab booking service page"""
    if 'email' not in request.session:
        return redirect('login')
    return render(request, 'services/cab.html')


def hotel(request):
    """Hotel reservation service page"""
    if 'email' not in request.session:
        return redirect('login')
    return render(request, 'services/hotel.html')


def fuel(request):
    """Fuel delivery service page"""
    if 'email' not in request.session:
        return redirect('login')
    return render(request, 'services/fuel.html')


def train(request):
    """Train ticket booking service page"""
    if 'email' not in request.session:
        return redirect('login')
    return render(request, 'services/train.html')


def flight(request):
    """Flight booking service page"""
    if 'email' not in request.session:
        return redirect('login')
    return render(request, 'services/flight.html')


def chatbot(request):
    """Groq-powered chatbot API endpoint (POST only)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            payload = {
                "model": getattr(settings, "GROQ_MODEL2"),
                "messages": [
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.2,
                "max_tokens": 200
            }

            headers = {
                "Authorization": f"Bearer {getattr(settings, 'GROQ_API_KEY2')}",
                "Content-Type": "application/json"
            }

            resp = requests.post(
                getattr(settings, "GROQ_API_URL2"),
                headers=headers, 
                json=payload, 
                timeout=60
            )

            resp_json = resp.json()
            reply = resp_json["choices"][0]["message"]["content"].strip()

            return JsonResponse({"response": reply})

        except Exception as e:
            return JsonResponse({"response": f"Error: {str(e)}"})

    return JsonResponse({'response': 'Invalid request method'}, status=405)


# ================= ONLINE STORE =================

def online_store(request):
    """Online store home page"""
    from .models import Product
    from django.db.models import Q
    
    if 'email' not in request.session:
        return redirect('login')
    
    # Base queryset - show all products including out of stock
    products = Product.objects.all()
    
    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Category Filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category=category_filter)
        
    # Sorting
    sort_option = request.GET.get('sort', 'newest')
    if sort_option == 'price_low':
        products = products.order_by('price')
    elif sort_option == 'price_high':
        products = products.order_by('-price')
    else: # newest
        products = products.order_by('-created_at')
    
    # Get categories for dropdown
    categories = Product.CATEGORY_CHOICES
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'sort_option': sort_option
    }
    
    return render(request, 'services/online_store.html', context)


def buy_product(request, product_id):
    """Handle product purchase"""
    from .models import Product, EcommerceOrder
    
    if 'email' not in request.session:
        return redirect('login')
    
    user = User.objects.get(email=request.session['email'])
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        payment_method = request.POST.get('payment_method', 'cod')
        upi_id = request.POST.get('upi_id', '')
        address = request.POST.get('address', '')
        
        if product.total_quantity < quantity:
            messages.error(request, 'Not enough stock available!')
            return redirect('online_store')
        
        # Calculate total price
        total_price = product.price * quantity
        
        # Create order
        EcommerceOrder.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            payment_method=payment_method,
            upi_id=upi_id if payment_method == 'upi' else None,
            address=address,
            total_price=total_price,
            status='pending'
        )
        
        # Reduce stock
        product.total_quantity -= quantity
        if product.total_quantity == 0:
            product.availability_status = False
        product.save()
        
        messages.success(request, f'Order for {product.product_name} placed successfully!')
        return redirect('online_bookings')
        
    return redirect('online_store')


def online_bookings(request):
    """User's ecommerce order history"""
    from .models import EcommerceOrder
    
    if 'email' not in request.session:
        return redirect('login')
    
    user = User.objects.get(email=request.session['email'])
    orders = EcommerceOrder.objects.filter(user=user).select_related('product').order_by('-created_at')
    
    return render(request, 'services/onlinebookings.html', {'orders': orders})


def cancel_order(request, order_id):
    """Cancel user's order"""
    from .models import EcommerceOrder
    
    if 'email' not in request.session:
        return redirect('login')
    
    user = User.objects.get(email=request.session['email'])
    order = get_object_or_404(EcommerceOrder, id=order_id, user=user)
    
    if order.status in ['pending', 'accepted']:
        # Restore stock
        product = order.product
        product.total_quantity += order.quantity
        if product.total_quantity > 0:
            product.availability_status = True
        product.save()
        
        # Update status
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel this order (it may have been shipped or already processed).')
        
    return redirect('online_bookings')


# ================= HOTEL BOOKING SYSTEM =================

def hotel_bookings(request):
    """User hotel booking page - create new bookings"""
    if 'email' not in request.session:
        return redirect('login')
    
    user = User.objects.get(email=request.session['email'])
    
    if request.method == 'POST':
        try:
            room_id = request.POST.get('room_id')
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')
            rooms_booked = int(request.POST.get('rooms_booked', 1))
            
            # Get room and validate
            room = get_object_or_404(Room, id=room_id)
            
            # Validate availability
            if rooms_booked > room.available_rooms:
                messages.error(request, f'Only {room.available_rooms} rooms available!')
                return redirect('hotel_bookings')
            
            # Validate dates
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            if check_out_date <= check_in_date:
                messages.error(request, 'Check-out date must be after check-in date!')
                return redirect('hotel_bookings')
            
            # Create booking
            booking = HotelBooking.objects.create(
                user=user,
                hotel=room.hotel,
                room=room,
                check_in=check_in_date,
                check_out=check_out_date,
                rooms_booked=rooms_booked,
                status='pending'
            )
            
            messages.success(request, 'Booking request sent. Waiting for hotel approval.')
            return redirect('my_bookings')
            
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
            return redirect('hotel_bookings')
    
    # GET request - show booking form
    # Only show approved hotels with rooms
    approved_hotels = Hotel.objects.filter(status='approved').prefetch_related('rooms')
    
    context = {
        'hotels': approved_hotels,
        'user': user
    }
    return render(request, 'services/hotel_bookings.html', context)


def my_bookings(request):
    """User's booking history page"""
    if 'email' not in request.session:
        return redirect('login')
    
    user = User.objects.get(email=request.session['email'])
    bookings = HotelBooking.objects.filter(user=user).select_related('hotel', 'room')
    
    context = {
        'bookings': bookings,
        'user': user
    }
    return render(request, 'services/my_bookings.html', context)


# ================= HOTEL ADMIN BOOKING MANAGEMENT =================

def hotel_admin_bookings(request):
    """Hotel admin booking management page"""
    if 'hotel_admin' not in request.session:
        messages.error(request, 'Please login as hotel admin first.')
        return redirect('hotel_admin_login')
    
    hotel = Hotel.objects.get(id=request.session['hotel_admin'])
    bookings = HotelBooking.objects.filter(hotel=hotel).select_related('user', 'room')
    
    # Calculate statistics
    pending_count = bookings.filter(status='pending').count()
    approved_count = bookings.filter(status='approved').count()
    rejected_count = bookings.filter(status='rejected').count()
    
    context = {
        'bookings': bookings,
        'hotel': hotel,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count
    }
    return render(request, 'hotel_admin/bookings.html', context)



def approve_booking(request, booking_id):
    """Approve a hotel booking - reduces room availability"""
    if 'hotel_admin' not in request.session:
        messages.error(request, 'Unauthorized')
        return redirect('hotel_admin_login')
    
    hotel = Hotel.objects.get(id=request.session['hotel_admin'])
    booking = get_object_or_404(HotelBooking, id=booking_id)
    
    # Authorization check - can only approve own hotel's bookings
    if booking.hotel.id != hotel.id:
        messages.error(request, 'You can only manage bookings for your own hotel!')
        return redirect('hotel_admin_bookings')
    
    # Check if already processed
    if booking.status != 'pending':
        messages.warning(request, f'Booking already {booking.status}!')
        return redirect('hotel_admin_bookings')
    
    # Check availability again
    if booking.rooms_booked > booking.room.available_rooms:
        messages.error(request, 'Not enough rooms available!')
        return redirect('hotel_admin_bookings')
    
    # Approve booking and reduce availability
    booking.status = 'approved'
    booking.save()
    
    booking.room.available_rooms -= booking.rooms_booked
    booking.room.save()
    
    messages.success(request, f'Booking approved! {booking.rooms_booked} room(s) allocated.')
    return redirect('hotel_admin_bookings')


def reject_booking(request, booking_id):
    """Reject a hotel booking - does not affect room availability"""
    if 'hotel_admin' not in request.session:
        messages.error(request, 'Unauthorized')
        return redirect('hotel_admin_login')
    
    hotel = Hotel.objects.get(id=request.session['hotel_admin'])
    booking = get_object_or_404(HotelBooking, id=booking_id)
    
    # Authorization check
    if booking.hotel.id != hotel.id:
        messages.error(request, 'You can only manage bookings for your own hotel!')
        return redirect('hotel_admin_bookings')
    
    # Check if already processed
    if booking.status != 'pending':
        messages.warning(request, f'Booking already {booking.status}!')
        return redirect('hotel_admin_bookings')
    
    # Reject booking - no room changes
    booking.status = 'rejected'
    booking.save()
    
    messages.success(request, 'Booking rejected.')
    return redirect('hotel_admin_bookings')


# ================= HOTEL ADMIN =================

def hotel_admin_register(request):
    if request.method == 'POST':
        if Hotel.objects.filter(email=request.POST.get('email')).exists():
            return HttpResponse("<script>alert('Email exists');window.location='/hotel-admin/register/'</script>")

        Hotel.objects.create(
            hotelowner=request.POST.get('hotelowner'),
            hotelname=request.POST.get('hotelname'),
            location=request.POST.get('location'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            password=request.POST.get('password')
        )
        return redirect('hotel_admin_login')

    return render(request, 'hotel_admin/register.html')


def hotel_admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            hotel = Hotel.objects.get(email=email, password=password)

            if hotel.status != 'approved':
                return HttpResponse(
                    "<script>alert('Your hotel is not approved yet'); window.location.href='/hotel-admin/login/';</script>"
                )

            request.session['hotel_admin'] = hotel.id
            return redirect('hotel_admin_dashboard')

        except Hotel.DoesNotExist:
            return HttpResponse(
                "<script>alert('Invalid credentials'); window.location.href='/hotel-admin/login/';</script>"
            )

    return render(request, 'hotel_admin/login.html')


def hotel_admin_dashboard(request):
    if 'hotel_admin' not in request.session:
        return redirect('hotel_admin_login')

    hotel = Hotel.objects.get(id=request.session['hotel_admin'])
    return render(request, 'hotel_admin/dashboard.html', {
        'hotels': [hotel]
    })


def hotel_admin_logout(request):
    request.session.flush()
    return redirect('hotel_admin_login')


# ================= ROOM MANAGEMENT =================

def add_room_type(request, hotel_id):
    if 'hotel_admin' not in request.session:
        return redirect('hotel_admin_login')

    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == 'POST':
        Room.objects.create(
            hotel=hotel,
            category=request.POST.get('category'),
            price_per_night=request.POST.get('price_per_night'),
            total_rooms=request.POST.get('total_rooms'),
            available_rooms=request.POST.get('available_rooms'),
            image=request.FILES.get('image')
        )
        return redirect('hotel_admin_dashboard')

    return render(request, 'hotel_admin/add_room.html', {'hotel': hotel})



def edit_room(request, room_id):
    if 'hotel_admin' not in request.session:
        return redirect('hotel_admin_login')

    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        room.category = request.POST.get('category')
        room.price_per_night = request.POST.get('price_per_night')
        room.total_rooms = request.POST.get('total_rooms')
        room.available_rooms = request.POST.get('available_rooms')

        if request.FILES.get('image'):
            room.image = request.FILES.get('image')

        room.save()
        return redirect('hotel_admin_dashboard')

    return render(request, 'hotel_admin/edit_room.html', {'room': room})



def delete_room(request, room_id):
    Room.objects.filter(id=room_id).delete()
    return redirect('hotel_admin_dashboard')


def delete_hotel(request, hotel_id):
    Hotel.objects.filter(id=hotel_id).delete()
    request.session.flush()
    return redirect('hotel_admin_login')

def upload_room_image(request, room_id):
    if 'hotel_admin' not in request.session:
        return redirect('hotel_admin_login')

    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST' and request.FILES.get('image'):
        room.image = request.FILES['image']
        room.save()
        return redirect('hotel_admin_dashboard')

    return render(request, 'hotel_admin/upload_image.html', {'room': room})


# ================= ONEHUB CUSTOM ADMIN =================

def onehub_admin_login(request):
    """Custom OneHub Admin Login - Hardcoded credentials"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin123':
            request.session['onehub_admin'] = username
            return redirect('onehub_admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'onehub_admin/login.html')


def onehub_admin_dashboard(request):
    """Custom OneHub Admin Dashboard"""
    from .models import EcommerceAdmin
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    users_count = User.objects.count()
    hotels_count = Hotel.objects.count()
    pending_hotels = Hotel.objects.filter(status='pending').count()
    approved_hotels = Hotel.objects.filter(status='approved').count()
    
    # Ecommerce statistics
    ecommerce_count = EcommerceAdmin.objects.count()
    pending_ecommerce = EcommerceAdmin.objects.filter(status='pending').count()
    approved_ecommerce = EcommerceAdmin.objects.filter(status='approved').count()

    context = {
        'users_count': users_count,
        'hotels_count': hotels_count,
        'pending_hotels': pending_hotels,
        'approved_hotels': approved_hotels,
        'ecommerce_count': ecommerce_count,
        'pending_ecommerce': pending_ecommerce,
        'approved_ecommerce': approved_ecommerce,
    }

    return render(request, 'onehub_admin/dashboard.html', context)


def onehub_admin_logout(request):
    """Custom OneHub Admin Logout"""
    request.session.flush()
    return redirect('onehub_admin_login')


def hotel_owners_list(request):
    """List all hotel owners with approval management"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    hotels = Hotel.objects.all().order_by('-id')
    return render(request, 'onehub_admin/hotel_owners.html', {'hotels': hotels})


def approve_hotel_owner(request, id):
    """Approve a hotel owner"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    hotel = get_object_or_404(Hotel, id=id)
    hotel.status = 'approved'
    hotel.save()
    messages.success(request, f'Hotel "{hotel.hotelowner}" has been approved')
    return redirect('hotel_owners_list')


def reject_hotel_owner(request, id):
    """Reject a hotel owner"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    hotel = get_object_or_404(Hotel, id=id)
    hotel.status = 'rejected'
    hotel.save()
    messages.warning(request, f'Hotel "{hotel.hotelowner}" has been rejected')
    return redirect('hotel_owners_list')


def delete_hotel_owner(request, id):
    """Delete a hotel owner"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    hotel = get_object_or_404(Hotel, id=id)
    hotel_name = hotel.hotelowner
    hotel.delete()
    messages.info(request, f'Hotel "{hotel_name}" has been deleted')
    return redirect('hotel_owners_list')


def users_list(request):
    """List all registered users"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    users = User.objects.all().order_by('-id')
    return render(request, 'onehub_admin/users_list.html', {'users': users})


def delete_user(request, id):
    """Delete a registered user"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    user = get_object_or_404(User, id=id)
    email = user.email
    user.delete()
    messages.success(request, f'User "{email}" has been deleted successfully.')
    return redirect('users_list')


# ================= OLD SUPER ADMIN (For backwards compatibility) =================

def super_admin_hotels(request):
    """Legacy function - redirects to new hotel_owners_list"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    hotels = Hotel.objects.all().order_by('-id')
    return render(request, 'onehub_admin/hotel_owners.html', {'hotels': hotels})


def approve_hotel(request, hotel_id):
    """Legacy function - redirects to approve_hotel_owner"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.status = 'approved'
    hotel.save()
    return redirect('hotel_owners_list')


def reject_hotel(request, hotel_id):
    """Legacy function - redirects to reject_hotel_owner"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.status = 'rejected'
    hotel.save()
    return redirect('hotel_owners_list')


# ================= ECOMMERCE ADMIN VIEWS =================

def ecommerce_register(request):
    """Handle ecommerce admin registration"""
    from .forms import RegistrationForm
    from .models import EcommerceAdmin
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create new admin with plain text password
            admin = EcommerceAdmin(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password']  # Store as plain text
            )
            admin.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('ecommerce_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = RegistrationForm()
    
    return render(request, 'ecommerce_admin/register.html', {'form': form})


def ecommerce_login(request):
    """Handle ecommerce admin login"""
    from .models import EcommerceAdmin
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            admin = EcommerceAdmin.objects.get(email=email)
            
            if password == admin.password:  # Direct comparison for plain text
                # Check approval status
                if admin.status != 'approved':
                    if admin.status == 'pending':
                        messages.warning(request, 'Your account is pending approval. Please wait for admin approval.')
                    elif admin.status == 'rejected':
                        messages.error(request, 'Your account has been rejected. Please contact support.')
                    return render(request, 'ecommerce_admin/login.html')
                
                # Create session
                request.session['ecommerce_admin_id'] = admin.id
                request.session['ecommerce_admin_name'] = admin.full_name
                messages.success(request, f'Welcome back, {admin.full_name}!')
                return redirect('ecommerce_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except EcommerceAdmin.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'ecommerce_admin/login.html')


def ecommerce_logout(request):
    """Handle ecommerce admin logout"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('ecommerce_login')


def ecommerce_dashboard(request):
    """Display dashboard with product statistics and list"""
    from .decorators import ecommerce_login_required
    from .models import Product, EcommerceAdmin
    
    if not request.session.get('ecommerce_admin_id'):
        return redirect('ecommerce_login')
    
    # Get current admin and their products only
    ecommerce_admin = get_object_or_404(EcommerceAdmin, id=request.session['ecommerce_admin_id'])
    products = Product.objects.filter(ecommerce_admin=ecommerce_admin)
    
    # Calculate statistics for current admin's products only
    total_products = products.count()
    available_products = products.filter(availability_status=True).count()
    out_of_stock_products = products.filter(availability_status=False).count()
    
    context = {
        'ecommerce_admin': ecommerce_admin,
        'products': products,
        'total_products': total_products,
        'available_products': available_products,
        'out_of_stock_products': out_of_stock_products,
        'admin_name': request.session.get('ecommerce_admin_name', 'Admin')
    }
    
    return render(request, 'ecommerce_admin/dashboard.html', context)


def ecommerce_add_product(request):
    """Handle adding new product"""
    from .forms import ProductForm
    from .models import EcommerceAdmin
    
    if not request.session.get('ecommerce_admin_id'):
        return redirect('ecommerce_login')
    
    # Get current admin
    ecommerce_admin = get_object_or_404(EcommerceAdmin, id=request.session['ecommerce_admin_id'])
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.ecommerce_admin = ecommerce_admin  # Link product to current admin
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('ecommerce_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm()
    
    return render(request, 'ecommerce_admin/add_product.html', {'form': form})


def ecommerce_edit_product(request, id):
    """Handle editing existing product"""
    from .forms import ProductForm
    from .models import Product, EcommerceAdmin
    
    if not request.session.get('ecommerce_admin_id'):
        return redirect('ecommerce_login')
    
    ecommerce_admin = get_object_or_404(EcommerceAdmin, id=request.session['ecommerce_admin_id'])
    product = get_object_or_404(Product, id=id)
    
    # Verify ownership - admin can only edit their own products
    if product.ecommerce_admin.id != ecommerce_admin.id:
        messages.error(request, 'You can only edit your own products!')
        return redirect('ecommerce_dashboard')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('ecommerce_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'ecommerce_admin/edit_product.html', {
        'form': form,
        'product': product
    })


def ecommerce_delete_product(request, id):
    """Handle deleting product"""
    from .models import Product, EcommerceAdmin
    
    if not request.session.get('ecommerce_admin_id'):
        return redirect('ecommerce_login')
    
    ecommerce_admin = get_object_or_404(EcommerceAdmin, id=request.session['ecommerce_admin_id'])
    product = get_object_or_404(Product, id=id)
    
    # Verify ownership - admin can only delete their own products
    if product.ecommerce_admin.id != ecommerce_admin.id:
        messages.error(request, 'You can only delete your own products!')
        return redirect('ecommerce_dashboard')
    
    product_name = product.product_name
    product.delete()
    messages.success(request, f'Product "{product_name}" deleted successfully!')
    return redirect('ecommerce_dashboard')


def ecommerce_orders(request):
    """Manage orders for ecommerce admin"""
    from .models import EcommerceAdmin, EcommerceOrder
    
    if not request.session.get('ecommerce_admin_id'):
        return redirect('ecommerce_login')
        
    ecommerce_admin = get_object_or_404(EcommerceAdmin, id=request.session['ecommerce_admin_id'])
    
    # Get orders for products owned by this admin
    orders = EcommerceOrder.objects.filter(product__ecommerce_admin=ecommerce_admin).select_related('product', 'user').order_by('-created_at')
    
    return render(request, 'ecommerce_admin/orders.html', {'orders': orders})


def ecommerce_update_order_status(request, order_id):
    """Update order status"""
    from .models import EcommerceOrder, EcommerceAdmin
    
    if not request.session.get('ecommerce_admin_id'):
        return redirect('ecommerce_login')
    
    ecommerce_admin = get_object_or_404(EcommerceAdmin, id=request.session['ecommerce_admin_id'])
    order = get_object_or_404(EcommerceOrder, id=order_id)
    
    # Verify ownership
    if order.product.ecommerce_admin.id != ecommerce_admin.id:
        messages.error(request, 'You can only manage orders for your own products!')
        return redirect('ecommerce_orders')
        
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}')
            
    return redirect('ecommerce_orders')


# ================= ECOMMERCE OWNER MANAGEMENT =================

def ecommerce_owners_list(request):
    """List all ecommerce owners with approval management"""
    from .models import EcommerceAdmin
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    ecommerce_admins = EcommerceAdmin.objects.all().order_by('-id')
    return render(request, 'onehub_admin/ecommerce_owners.html', {'ecommerce_admins': ecommerce_admins})


def approve_ecommerce_owner(request, id):
    """Approve an ecommerce owner"""
    from .models import EcommerceAdmin
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    admin = get_object_or_404(EcommerceAdmin, id=id)
    admin.status = 'approved'
    admin.save()
    messages.success(request, f'Ecommerce admin "{admin.full_name}" has been approved!')
    return redirect('ecommerce_owners_list')


def reject_ecommerce_owner(request, id):
    """Reject an ecommerce owner"""
    from .models import EcommerceAdmin
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    admin = get_object_or_404(EcommerceAdmin, id=id)
    admin.status = 'rejected'
    admin.save()
    messages.warning(request, f'Ecommerce admin "{admin.full_name}" has been rejected.')
    return redirect('ecommerce_owners_list')


def delete_ecommerce_owner(request, id):
    """Delete an ecommerce owner"""
    from .models import EcommerceAdmin
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')

    admin = get_object_or_404(EcommerceAdmin, id=id)
    admin_name = admin.full_name
    admin.delete()
    messages.info(request, f'Ecommerce admin "{admin_name}" has been deleted.')
    return redirect('ecommerce_owners_list')
def submit_hotel_review(request, hotel_id):
    """Handle 5-star rating and review submission for hotels"""
    if 'email' not in request.session:
        return JsonResponse({'error': 'Please login to submit a review'}, status=401)
    
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.session['email'])
            hotel = get_object_or_404(Hotel, id=hotel_id)
            rating_value = int(request.POST.get('rating', 5))
            comment = request.POST.get('comment', '')
            
            # Create or update rating
            rating, created = HotelRating.objects.update_or_create(
                user=user,
                hotel=hotel,
                defaults={'rating': rating_value, 'comment': comment}
            )
            
            messages.success(request, f'Thank you for rating {hotel.hotelowner}!')
            return redirect('hotel_bookings')
            
        except Exception as e:
            messages.error(request, f'Error submitting review: {str(e)}')
            return redirect('hotel_bookings')
            
    return redirect('hotel_bookings')


# ================= TOURIST PLACES VIEWS =================

def tourist_places_list(request):
    """List all tourist places"""
    from .models import TouristPlace
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')
    
    places = TouristPlace.objects.all().prefetch_related('images')
    
    context = {
        'places': places
    }
    
    return render(request, 'onehub_admin/tourist_places.html', context)



def add_tourist_place(request):
    """Add a new tourist place"""
    from .forms import TouristPlaceForm
    from .models import TouristPlace, TouristPlaceImage
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')
    
    if request.method == 'POST':
        form = TouristPlaceForm(request.POST)
        if form.is_valid():
            place = form.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for image in images:
                TouristPlaceImage.objects.create(
                    tourist_place=place,
                    image=image
                )
            
            messages.success(request, f'Tourist place "{place.name}" added successfully!')
            return redirect('tourist_places_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('tourist_places_list')


def edit_tourist_place(request, id):
    """Edit an existing tourist place"""
    from .forms import TouristPlaceForm
    from .models import TouristPlace, TouristPlaceImage
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')
    
    place = get_object_or_404(TouristPlace, id=id)
    
    if request.method == 'POST':
        form = TouristPlaceForm(request.POST, instance=place)
        if form.is_valid():
            place = form.save()
            
            # Handle new image uploads
            images = request.FILES.getlist('images')
            for image in images:
                TouristPlaceImage.objects.create(
                    tourist_place=place,
                    image=image
                )
            
            messages.success(request, f'Tourist place "{place.name}" updated successfully!')
            return redirect('tourist_places_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('tourist_places_list')


def delete_tourist_place(request, id):
    """Delete a tourist place"""
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')
    
    place = get_object_or_404(TouristPlace, id=id)
    place_name = place.name
    place.delete()
    messages.success(request, f'Tourist place "{place_name}" has been deleted.')
    return redirect('tourist_places_list')


def delete_tourist_image(request, image_id):
    """Delete a specific tourist place image"""
    from .models import TouristPlaceImage
    
    if not request.session.get('onehub_admin'):
        return redirect('onehub_admin_login')
    
    image = get_object_or_404(TouristPlaceImage, id=image_id)
    image.delete()
    messages.success(request, 'Image deleted successfully!')
    return redirect('tourist_places_list')


# ================= USER-FACING TOURIST PLACES =================

def tourist_places(request):
    """Display all active tourist places for regular users"""
    from .models import TouristPlace
    
    # Only show active places to users
    places = TouristPlace.objects.filter(is_active=True).prefetch_related('images').order_by('-created_at')
    
    context = {
        'places': places
    }
    
    return render(request, 'tourist_destinations.html', context)
