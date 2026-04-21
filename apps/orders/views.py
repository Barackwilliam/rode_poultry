from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

from apps.products.models import Product
from .cart import Cart
from .models import Order, OrderItem, PromoCode


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
    messages.success(request, f'{product.name} imeongezwa kwenye Cart.')
    return redirect('orders:cart')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('orders:cart')


def validate_promo(request):
    """AJAX endpoint to validate a promo code."""
    if request.method == 'GET':
        code = request.GET.get('code', '').strip().upper()
        subtotal = float(request.GET.get('subtotal', 0))
        try:
            promo = PromoCode.objects.get(code=code, is_active=True)
            discount = round(subtotal * promo.discount_percent / 100, 2)
            return JsonResponse({
                'valid': True,
                'percent': promo.discount_percent,
                'discount': discount,
                'message': f'Kodi sahihi! Punguzo la {promo.discount_percent}% — TSH {discount:,.0f}'
            })
        except PromoCode.DoesNotExist:
            return JsonResponse({'valid': False, 'message': 'Kodi si sahihi au imekwisha.'})
    return JsonResponse({'valid': False})


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Cart yako iko tupu.')
        return redirect('products:list')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        region = request.POST.get('region', 'Morogoro').strip()
        notes = request.POST.get('notes', '').strip()
        payment_method = request.POST.get('payment_method', 'cod').strip()
        promo_code = request.POST.get('promo_code', '').strip().upper()

        if not all([full_name, phone, address]):
            messages.error(request, 'Tafadhali jaza sehemu zote zinazohitajika (*).')
            return render(request, 'orders/checkout.html', {'cart': cart})

        subtotal = cart.get_total_price()
        delivery_fee = round(float(subtotal) * 0.05, 2)  # 5% ya thamani - owner anabadilisha
        discount_amount = 0

        # Validate promo code
        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code, is_active=True)
                discount_amount = round(float(subtotal) * promo.discount_percent / 100, 2)
            except PromoCode.DoesNotExist:
                messages.warning(request, 'Kodi ya punguzo si sahihi, inaendelea bila punguzo.')
                promo_code = ''

        total = float(subtotal) + delivery_fee - discount_amount

        # Deposit calculation for 70/30 option
        deposit_amount = 0
        balance_due = 0
        if payment_method == 'deposit':
            deposit_amount = round(total * 0.70, 2)
            balance_due = round(total * 0.30, 2)

        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            region=region,
            notes=notes,
            payment_method=payment_method,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            discount_amount=discount_amount,
            discount_code=promo_code,
            total_amount=total,
            deposit_amount=deposit_amount,
            balance_due=balance_due,
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
            payment_label = dict(Order.PAYMENT_METHOD_CHOICES).get(payment_method, payment_method)
            deposit_note = f'\nAmana ya kulipa: TSH {deposit_amount:,.0f}\nBaki siku ya kupokea: TSH {balance_due:,.0f}' if payment_method == 'deposit' else ''
            send_mail(
                subject=f'Oda Mpya #{order.pk} kutoka {order.full_name}',
                message=(
                    f'Oda #{order.pk}\n'
                    f'Mteja: {order.full_name}\n'
                    f'Simu: {order.phone}\n'
                    f'Email: {order.email}\n'
                    f'Anwani: {order.address}, {order.region}\n'
                    f'Maelezo: {order.notes}\n\n'
                    f'Bidhaa:\n{items_text}\n\n'
                    f'Jumla Ndogo: TSH {subtotal:,.0f}\n'
                    f'Gharama za Usafiri: TSH {delivery_fee:,.0f}\n'
                    f'Punguzo: TSH {discount_amount:,.0f} (Kodi: {promo_code})\n'
                    f'JUMLA: TSH {total:,.0f}\n'
                    f'Malipo: {payment_label}{deposit_note}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.COMPANY_EMAIL],
            )
        except Exception:
            pass

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
            messages.error(request, 'Oda haikupatikana. Angalia namba ya oda na simu yako.')
    return render(request, 'orders/tracking.html', {'order': order})

