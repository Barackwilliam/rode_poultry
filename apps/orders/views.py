from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

from apps.products.models import Product
from .cart import Cart
from .models import Order, OrderItem


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override', False)
    cart.add(product=product, quantity=quantity, override_quantity=bool(override))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': len(cart), 'message': 'Added to cart'})
    messages.success(request, f'{product.name} added to cart.')
    return redirect('orders:cart')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('orders:cart')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('products:list')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        region = request.POST.get('region', 'Morogoro').strip()
        notes = request.POST.get('notes', '').strip()

        if not all([full_name, email, phone, address]):
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'orders/checkout.html', {'cart': cart})

        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            region=region,
            notes=notes,
            total_amount=cart.get_total_price(),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
            )

        cart.clear()

        # Notify admin
        try:
            items_text = '\n'.join(
                f"- {oi.product_name} x{oi.quantity} @ TSH {oi.price:,.0f}"
                for oi in order.items.all()
            )
            send_mail(
                subject=f'New Order #{order.pk} from {order.full_name}',
                message=(
                    f'Order #{order.pk}\n'
                    f'Customer: {order.full_name}\n'
                    f'Phone: {order.phone}\n'
                    f'Email: {order.email}\n'
                    f'Address: {order.address}, {order.region}\n'
                    f'Notes: {order.notes}\n\n'
                    f'Items:\n{items_text}\n\n'
                    f'TOTAL: TSH {order.total_amount:,.0f}\n'
                    f'Payment: Cash on Delivery'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.COMPANY_EMAIL],
            )
        except Exception:
            pass  # Don't block order on email failure

        return redirect('orders:order_success', order_id=order.pk)

    return render(request, 'orders/checkout.html', {'cart': cart})


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/success.html', {'order': order})


def order_tracking(request):
    order = None
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        phone = request.POST.get('phone')
        try:
            order = Order.objects.get(pk=order_id, phone=phone)
        except Order.DoesNotExist:
            messages.error(request, 'Order not found. Please check your Order ID and phone number.')
    return render(request, 'orders/tracking.html', {'order': order})
