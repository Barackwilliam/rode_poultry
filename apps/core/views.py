from django.shortcuts import render
from apps.products.models import Product, Category
from apps.gallery.models import GalleryMedia


def home(request):
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:6]
    categories = Category.objects.all()
    latest_media = GalleryMedia.objects.filter(is_active=True).order_by('-created_at')[:6]
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_media': latest_media,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    from django.contrib import messages
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # Send email notification
        from django.core.mail import send_mail
        from django.conf import settings
        try:
            send_mail(
                subject=f'New Contact from {name} - Rode Poultry Website',
                message=f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.COMPANY_EMAIL],
            )
            messages.success(request, 'Your message has been sent successfully! We will contact you soon.')
        except Exception:
            messages.error(request, 'There was an error sending your message. Please try again.')
        from django.shortcuts import redirect
        return redirect('core:contact')
    return render(request, 'core/contact.html')
