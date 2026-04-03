"""
API Integration Services for ONEHUB
Handles API calls to various service providers (Food, Cab, Flight, Train, Hotel, Fuel)
Uses mock APIs with real API structure for demonstration
"""
import requests
import json
import os
from typing import Dict, List, Optional
from django.conf import settings


class FoodDeliveryService:
    """Food Delivery API Integration (Zomato, Swiggy, Uber Eats)"""
    
    @staticmethod
    def search_food(query: str, latitude: float = None, longitude: float = None) -> List[Dict]:
        """
        Search for food items across multiple providers
        Returns aggregated results from Zomato, Swiggy, and Uber Eats
        """
        results = []
        
        # Mock Zomato API
        zomato_results = [
            {
                'provider': 'Zomato',
                'restaurant_name': f'{query.title()} Place',
                'item': query,
                'price': 250,
                'delivery_time': '25 min',
                'rating': 4.3,
                'distance': '1.2 km',
                'url': 'https://www.zomato.com/order',
                'logo': '/static/images/zomato.png'
            },
            {
                'provider': 'Zomato',
                'restaurant_name': f'Best {query.title()}',
                'item': query,
                'price': 280,
                'delivery_time': '30 min',
                'rating': 4.5,
                'distance': '2.1 km',
                'url': 'https://www.zomato.com/order',
                'logo': '/static/images/zomato.png'
            }
        ]
        
        # Mock Swiggy API
        swiggy_results = [
            {
                'provider': 'Swiggy',
                'restaurant_name': f'{query.title()} Hub',
                'item': query,
                'price': 240,
                'delivery_time': '20 min',
                'rating': 4.4,
                'distance': '0.8 km',
                'url': 'https://www.swiggy.com/order',
                'logo': '/static/images/swiggy.png'
            },
            {
                'provider': 'Swiggy',
                'restaurant_name': f'Premium {query.title()}',
                'item': query,
                'price': 300,
                'delivery_time': '35 min',
                'rating': 4.6,
                'distance': '3.5 km',
                'url': 'https://www.swiggy.com/order',
                'logo': '/static/images/swiggy.png'
            }
        ]
        
        # Mock Uber Eats API
        ubereats_results = [
            {
                'provider': 'Uber Eats',
                'restaurant_name': f'{query.title()} Express',
                'item': query,
                'price': 260,
                'delivery_time': '22 min',
                'rating': 4.2,
                'distance': '1.5 km',
                'url': 'https://www.ubereats.com/order',
                'logo': '/static/images/uber-eats.png'
            }
        ]
        
        results.extend(zomato_results)
        results.extend(swiggy_results)
        results.extend(ubereats_results)
        
        # Sort by price
        results.sort(key=lambda x: x['price'])
        
        return results


class CabBookingService:
    """Cab Booking API Integration (Uber, Ola)"""
    
    @staticmethod
    def search_cabs(pickup_lat: float, pickup_lng: float, 
                    drop_lat: float = None, drop_lng: float = None) -> List[Dict]:
        """
        Search for available cabs across Uber and Ola
        """
        results = []
        
        # Mock Uber API
        uber_cabs = [
            {
                'provider': 'Uber',
                'cab_type': 'UberGo',
                'price': 120,
                'eta': '5 min',
                'distance': '2.3 km',
                'url': 'https://www.uber.com/book',
                'logo': '/static/images/uber.avif'
            },
            {
                'provider': 'Uber',
                'cab_type': 'UberX',
                'price': 150,
                'eta': '6 min',
                'distance': '2.5 km',
                'url': 'https://www.uber.com/book',
                'logo': '/static/images/uber.avif'
            },
            {
                'provider': 'Uber',
                'cab_type': 'UberPremier',
                'price': 200,
                'eta': '7 min',
                'distance': '2.8 km',
                'url': 'https://www.uber.com/book',
                'logo': '/static/images/uber.avif'
            }
        ]
        
        # Mock Ola API
        ola_cabs = [
            {
                'provider': 'Ola',
                'cab_type': 'Mini',
                'price': 110,
                'eta': '4 min',
                'distance': '2.1 km',
                'url': 'https://www.olacabs.com/book',
                'logo': '/static/images/ola.png'
            },
            {
                'provider': 'Ola',
                'cab_type': 'Sedan',
                'price': 140,
                'eta': '5 min',
                'distance': '2.4 km',
                'url': 'https://www.olacabs.com/book',
                'logo': '/static/images/ola.png'
            },
            {
                'provider': 'Ola',
                'cab_type': 'Prime',
                'price': 180,
                'eta': '6 min',
                'distance': '2.6 km',
                'url': 'https://www.olacabs.com/book',
                'logo': '/static/images/ola.png'
            }
        ]
        
        results.extend(uber_cabs)
        results.extend(ola_cabs)
        
        # Sort by price
        results.sort(key=lambda x: x['price'])
        
        return results


class FlightBookingService:
    """Flight Booking API Integration"""
    
    @staticmethod
    def search_flights(source: str, destination: str, date: str) -> List[Dict]:
        """
        Search for available flights
        """
        results = [
            {
                'provider': 'MakeMyTrip',
                'airline': 'IndiGo',
                'flight_number': '6E-234',
                'departure_time': '08:30',
                'arrival_time': '10:45',
                'duration': '2h 15m',
                'price': 4500,
                'url': 'https://www.makemytrip.com/flights',
                'logo': '/static/images/mmt.png'
            },
            {
                'provider': 'Goibibo',
                'airline': 'Air India',
                'flight_number': 'AI-567',
                'departure_time': '10:15',
                'arrival_time': '12:30',
                'duration': '2h 15m',
                'price': 4800,
                'url': 'https://www.goibibo.com/flights',
                'logo': '/static/images/goibibo.png'
            },
            {
                'provider': 'Yatra',
                'airline': 'SpiceJet',
                'flight_number': 'SG-789',
                'departure_time': '14:20',
                'arrival_time': '16:35',
                'duration': '2h 15m',
                'price': 4200,
                'url': 'https://www.yatra.com/flights',
                'logo': '/static/images/yatra.png'
            }
        ]
        
        results.sort(key=lambda x: x['price'])
        return results


class TrainBookingService:
    """Train Booking API Integration"""
    
    @staticmethod
    def search_trains(source: str, destination: str, date: str) -> List[Dict]:
        """
        Search for available trains
        """
        results = [
            {
                'provider': 'IRCTC',
                'train_name': 'Rajdhani Express',
                'train_number': '12301',
                'departure_time': '17:00',
                'arrival_time': '06:30',
                'duration': '13h 30m',
                'price': 1850,
                'class': '3A',
                'url': 'https://www.irctc.co.in',
                'logo': '/static/images/irctc.png'
            },
            {
                'provider': 'IRCTC',
                'train_name': 'Shatabdi Express',
                'train_number': '12001',
                'departure_time': '06:00',
                'arrival_time': '14:30',
                'duration': '8h 30m',
                'price': 1650,
                'class': 'CC',
                'url': 'https://www.irctc.co.in',
                'logo': '/static/images/irctc.png'
            },
            {
                'provider': 'Paytm',
                'train_name': 'Duronto Express',
                'train_number': '12259',
                'departure_time': '23:00',
                'arrival_time': '10:00',
                'duration': '11h 00m',
                'price': 1750,
                'class': 'SL',
                'url': 'https://paytm.com/train-tickets',
                'logo': '/static/images/paytm.png'
            }
        ]
        
        results.sort(key=lambda x: x['price'])
        return results


class HotelBookingService:
    """Hotel Booking API Integration"""
    
    @staticmethod
    def search_hotels(location: str, check_in: str, check_out: str, guests: int = 2) -> List[Dict]:
        """
        Search for available hotels
        """
        results = [
            {
                'provider': 'Booking.com',
                'hotel_name': 'Grand Plaza',
                'location': location,
                'price_per_night': 2500,
                'rating': 4.5,
                'amenities': ['WiFi', 'Pool', 'Gym'],
                'url': 'https://www.booking.com',
                'logo': '/static/images/booking.png'
            },
            {
                'provider': 'OYO',
                'hotel_name': 'OYO Premium',
                'location': location,
                'price_per_night': 1800,
                'rating': 4.2,
                'amenities': ['WiFi', 'AC'],
                'url': 'https://www.oyorooms.com',
                'logo': '/static/images/oyo.png'
            },
            {
                'provider': 'MakeMyTrip',
                'hotel_name': 'Comfort Inn',
                'location': location,
                'price_per_night': 2200,
                'rating': 4.3,
                'amenities': ['WiFi', 'Pool', 'Breakfast'],
                'url': 'https://www.makemytrip.com/hotels',
                'logo': '/static/images/mmt.png'
            }
        ]
        
        results.sort(key=lambda x: x['price_per_night'])
        return results


class FuelDeliveryService:
    """Fuel Delivery API Integration"""
    
    @staticmethod
    def search_fuel_delivery(latitude: float, longitude: float, fuel_type: str = 'Petrol') -> List[Dict]:
        """
        Search for fuel delivery services
        """
        results = [
            {
                'provider': 'IndianOil',
                'service_name': 'IndianOil Xpress',
                'fuel_type': fuel_type,
                'price_per_liter': 95.5,
                'delivery_time': '30 min',
                'min_quantity': 5,
                'distance': '2.5 km',
                'url': 'https://www.iocl.com/fuel-delivery',
                'logo': '/static/images/indianoil.png'
            },
            {
                'provider': 'HPCL',
                'service_name': 'HPCL Home Delivery',
                'fuel_type': fuel_type,
                'price_per_liter': 96.0,
                'delivery_time': '25 min',
                'min_quantity': 5,
                'distance': '1.8 km',
                'url': 'https://www.hindustanpetroleum.com/fuel-delivery',
                'logo': '/static/images/hpcl.png'
            },
            {
                'provider': 'BPCL',
                'service_name': 'BPCL Doorstep',
                'fuel_type': fuel_type,
                'price_per_liter': 95.8,
                'delivery_time': '35 min',
                'min_quantity': 5,
                'distance': '3.2 km',
                'url': 'https://www.bharatpetroleum.com/fuel-delivery',
                'logo': '/static/images/bpcl.png'
            }
        ]
        
        results.sort(key=lambda x: x['price_per_liter'])
        return results

