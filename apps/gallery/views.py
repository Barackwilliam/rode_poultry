from django.shortcuts import render
from .models import GalleryMedia, GalleryCategory


def gallery(request):
    categories = GalleryCategory.objects.all()
    media = GalleryMedia.objects.filter(is_active=True)
    cat_slug = request.GET.get('category')
    media_type = request.GET.get('type')
    active_category = None
    if cat_slug:
        active_category = categories.filter(slug=cat_slug).first()
        if active_category:
            media = media.filter(category=active_category)
    if media_type in ['image', 'youtube']:
        media = media.filter(media_type=media_type)
    return render(request, 'gallery/gallery.html', {
        'media': media,
        'categories': categories,
        'active_category': active_category,
        'media_type': media_type,
    })
