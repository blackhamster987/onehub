# ONEHUB - Unified Service Platform

ONEHUB is a full-stack Django web application that aggregates multiple everyday services into a single, unified dashboard. The platform allows users to compare prices and options across different service providers and redirects them to the official provider apps/websites for final booking.

## Features

### Core Services
1. **Food Delivery** - Compare prices across Zomato, Swiggy, and Uber Eats
2. **Cab Booking** - Compare Uber and Ola with pricing and ETA
3. **Flight Booking** - Search and compare flights across multiple providers
4. **Train Booking** - Find and book train tickets with price comparison
5. **Hotel Reservations** - Compare hotel prices and amenities
6. **Fuel Delivery** - Find nearby fuel delivery services

### AI Chatbot
- Integrated Google Gemini API for natural language queries
- Understands user intent and navigates to appropriate services
- Example queries: "Order biryani from nearest place", "Book a cab to airport", "Find cheapest flight tomorrow"

### User Features
- User registration and authentication
- User profile management
- Unified dashboard with all services
- Location-based service discovery (geolocation)
- Price comparison across providers
- Direct redirection to provider apps/websites

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
```bash
cd /path/to/onehub
```

2. **Create a virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   - Create a `.env` file in the project root (optional, you can use system environment variables)
   - Add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   - Get your API key from: https://makersuite.google.com/app/apikey

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser (optional, for admin access)**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Access the application**
   - Open your browser and go to: http://127.0.0.1:8000/

## Project Structure

```
onehub/
├── onehub/              # Django project settings
│   ├── settings.py      # Project settings
│   ├── urls.py          # Root URL configuration
│   └── ...
├── onehub_app/          # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # App URL routing
│   ├── services.py      # API integration services
│   ├── chatbot.py       # Gemini chatbot integration
│   ├── templates/       # HTML templates
│   │   ├── services/    # Service-specific templates
│   │   └── ...
│   └── static/          # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── db.sqlite3           # SQLite database
├── requirements.txt     # Python dependencies
└── manage.py           # Django management script
```

## Usage

### For Users

1. **Register/Login**: Create an account or login to access the dashboard
2. **Explore Services**: Browse services from the unified dashboard
3. **Search**: Use the AI chatbot or search directly in service pages
4. **Compare**: View prices and options across different providers
5. **Book**: Click "Order Now" or "Book Now" to be redirected to the provider's official app/website

### For Developers

#### Adding New Services
1. Add a new service class in `onehub_app/services.py`
2. Create a view function in `onehub_app/views.py`
3. Add URL route in `onehub_app/urls.py`
4. Create a template in `onehub_app/templates/services/`
5. Add service card to dashboard template

#### API Integration
- Services use mock APIs by default
- Replace mock data with real API calls in `services.py`
- Update environment variables for API keys as needed

#### Chatbot Customization
- Modify `onehub_app/chatbot.py` to customize AI responses
- Update the fallback processor for better rule-based handling
- Adjust the Gemini API prompt for different behaviors

## API Keys

### Google Gemini API
- Get your API key from: https://makersuite.google.com/app/apikey
- Set it in `.env` file as `GEMINI_API_KEY=your_key`
- Or set as system environment variable

### Service Provider APIs (Optional)
To integrate real APIs:
- **Zomato**: https://developers.zomato.com/api
- **Swiggy**: Contact for API access
- **Uber**: https://developer.uber.com/
- **Ola**: Contact for API access
- **IRCTC**: https://www.irctc.co.in/nget/train-search
- **Flight APIs**: MakeMyTrip, Goibibo, etc.

## Technical Stack

- **Backend**: Django 4.2+, Django REST Framework (ready for API expansion)
- **Frontend**: Django Templates, Tailwind CSS
- **Database**: SQLite (default), can be switched to PostgreSQL/MySQL
- **AI**: Google Gemini API
- **Location Services**: Browser Geolocation API

## Security Notes

- Use environment variables for sensitive data (API keys, secrets)
- In production, set `DEBUG = False` in settings.py
- Use a strong `SECRET_KEY` in production
- Implement proper password hashing (currently using plain text - upgrade for production)
- Add CSRF protection (already included)
- Use HTTPS in production

## Future Enhancements

- Payment gateway integration (currently redirects to providers)
- Real-time API integrations with all providers
- Mobile app development
- Advanced filtering and sorting options
- User favorites and history
- Notifications and reminders
- Social sharing features

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, please refer to the Django documentation:
- Django: https://docs.djangoproject.com/
- Google Gemini: https://ai.google.dev/docs

---

**Built with ❤️ for seamless daily life management**

