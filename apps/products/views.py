from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    category_slug = request.GET.get('category')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)
    search = request.GET.get('q')
    if search:
        products = products.filter(name__icontains=search) | products.filter(name_sw__icontains=search)
    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'search_query': search or '',
    }
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = Product.objects.filter(category=product.category, is_available=True).exclude(pk=product.pk)[:4]
    return render(request, 'products/detail.html', {'product': product, 'related': related})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)
    return render(request, 'products/category.html', {'category': category, 'products': products})
