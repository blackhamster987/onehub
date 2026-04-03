from django.shortcuts import redirect
from functools import wraps


def ecommerce_login_required(view_func):
    """
    Decorator to check if ecommerce admin is logged in.
    Redirects to login page if not authenticated.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('ecommerce_admin_id'):
            return redirect('ecommerce_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def food_admin_login_required(view_func):
    """
    Decorator to check if food admin is logged in.
    Redirects to login page if not authenticated.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('food_admin_id'):
            return redirect('food_admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

