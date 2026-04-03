"""
AI Chatbot Service using Google Gemini API
Handles conversational queries and routes users to appropriate services
"""
import os
import json
from typing import Dict, Optional
from django.conf import settings

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class OneHubChatbot:
    """Chatbot service using Google Gemini API"""
    
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY', '')
        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def process_query(self, user_query: str) -> Dict:
        """
        Process user query and determine intent
        Returns action to take (service, search params, etc.)
        """
        if not self.model:
            # Fallback to rule-based system if Gemini is not available
            return self._fallback_processor(user_query)
        
        try:
            prompt = f"""You are a helpful assistant for ONEHUB, a unified service platform.
Analyze the user's query and extract the intent and parameters.

Available services:
1. Food Delivery - keywords: order, food, biryani, pizza, delivery, restaurant
2. Cab Booking - keywords: cab, taxi, ride, uber, ola, airport, travel
3. Flight Booking - keywords: flight, fly, plane, airport
4. Train Booking - keywords: train, railway, ticket
5. Hotel Booking - keywords: hotel, stay, accommodation, room
6. Fuel Delivery - keywords: fuel, petrol, diesel, gas

User Query: "{user_query}"

Respond ONLY with valid JSON in this exact format:
{{
    "service": "food|cab|flight|train|hotel|fuel|general",
    "action": "search|navigate|redirect",
    "parameters": {{
        "query": "search term if applicable",
        "source": "for flights/trains/cabs",
        "destination": "for flights/trains/cabs",
        "date": "YYYY-MM-DD format if mentioned",
        "location": "location if mentioned"
    }},
    "response": "A helpful response to the user",
    "redirect_url": "URL to navigate to if action is redirect"
}}"""

            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response (sometimes Gemini wraps it in markdown)
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            result = json.loads(result_text)
            return result
            
        except Exception as e:
            # Fallback on error
            return self._fallback_processor(user_query)
    
    def _fallback_processor(self, user_query: str) -> Dict:
        """Fallback rule-based processor when Gemini is not available"""
        query_lower = user_query.lower()
        
        # Food delivery
        if any(word in query_lower for word in ['order', 'food', 'biryani', 'pizza', 'delivery', 'restaurant', 'hungry']):
            query_term = query_lower
            for word in ['order', 'food', 'delivery', 'from', 'the', 'nearest', 'place']:
                query_term = query_term.replace(word, '').strip()
            
            return {
                'service': 'food',
                'action': 'search',
                'parameters': {
                    'query': query_term if query_term else 'food'
                },
                'response': f"I'll help you find {query_term if query_term else 'food'} from nearby restaurants.",
                'redirect_url': '/food/'
            }
        
        # Cab booking
        elif any(word in query_lower for word in ['cab', 'taxi', 'ride', 'uber', 'ola', 'airport']):
            destination = 'airport' if 'airport' in query_lower else None
            return {
                'service': 'cab',
                'action': 'search',
                'parameters': {
                    'destination': destination
                },
                'response': 'I\'ll help you book a cab. Please provide your pickup location.',
                'redirect_url': '/cab/'
            }
        
        # Flight booking
        elif any(word in query_lower for word in ['flight', 'fly', 'plane', 'airplane']):
            return {
                'service': 'flight',
                'action': 'search',
                'parameters': {},
                'response': 'I\'ll help you find flights. Please provide source and destination.',
                'redirect_url': '/flight/'
            }
        
        # Train booking
        elif any(word in query_lower for word in ['train', 'railway', 'rail']):
            return {
                'service': 'train',
                'action': 'search',
                'parameters': {},
                'response': 'I\'ll help you book train tickets. Please provide source and destination.',
                'redirect_url': '/train/'
            }
        
        # Hotel booking
        elif any(word in query_lower for word in ['hotel', 'stay', 'accommodation', 'room']):
            return {
                'service': 'hotel',
                'action': 'search',
                'parameters': {},
                'response': 'I\'ll help you find hotels. Please provide location and dates.',
                'redirect_url': '/hotel/'
            }
        
        # Fuel delivery
        elif any(word in query_lower for word in ['fuel', 'petrol', 'diesel', 'gas']):
            return {
                'service': 'fuel',
                'action': 'search',
                'parameters': {},
                'response': 'I\'ll help you find fuel delivery services nearby.',
                'redirect_url': '/fuel/'
            }
        
        # General response
        else:
            return {
                'service': 'general',
                'action': 'navigate',
                'parameters': {},
                'response': 'I can help you with food delivery, cab booking, flights, trains, hotels, and fuel delivery. What would you like to do?',
                'redirect_url': None
            }

