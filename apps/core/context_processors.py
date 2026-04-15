from django.conf import settings


def cart_count(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    count = sum(item['quantity'] for item in cart.values())
    return {'cart_count': count}


def site_settings(request):
    return {
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_EMAIL': settings.COMPANY_EMAIL,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_LOCATION': settings.COMPANY_LOCATION,
    }
