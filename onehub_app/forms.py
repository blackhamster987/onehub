from django import forms
from .models import Product, EcommerceAdmin, TouristPlace, TouristPlaceImage
from django.contrib.auth.hashers import make_password


class RegistrationForm(forms.Form):
    """Registration form for ecommerce admins"""
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if EcommerceAdmin.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        """Validate password length"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        if password and len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        
        return cleaned_data


class ProductForm(forms.ModelForm):
    """Form for adding/editing products"""
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'category', 'price', 
                  'image', 'total_quantity', 'availability_status']
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'step': '0.01'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'total_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter total quantity'
            }),
            'availability_status': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


# ================= TOURIST PLACES FORMS =================

class TouristPlaceForm(forms.ModelForm):
    """Form for adding/editing tourist places"""
    class Meta:
        model = TouristPlace
        fields = ['name', 'description', 'opening_time', 'location_link', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tourist place name',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional description',
                'rows': 4
            }),
            'opening_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 9:00 AM - 6:00 PM or 24 hours'
            }),
            'location_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Google Maps URL or location link'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class TouristPlaceImageForm(forms.ModelForm):
    """Form for uploading images"""
    class Meta:
        model = TouristPlaceImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
