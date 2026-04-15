from django.contrib import admin
from .models import GalleryMedia, GalleryCategory
from .forms import GalleryMediaAdminForm

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_sw', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GalleryMedia)
class GalleryMediaAdmin(admin.ModelAdmin):
    form = GalleryMediaAdminForm
    list_display = ['title', 'media_type', 'category', 'is_active', 'order', 'created_at']
    list_editable = ['is_active', 'order']
    list_filter = ['media_type', 'category', 'is_active']
    search_fields = ['title', 'title_sw']

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)

        # Kwenye model yako field inaitwa 'image_url'
        if db_field.name == "image":
            formfield.widget.attrs.update({
                "role": "uploadcare-uploader",
                "data-public-key": "431f160fc3fcf0ffb783",
                "data-images-only": "true",
            })
        return formfield

    def image_preview(self, obj):
        if obj.image:
            url = f"https://ucarecdn.com/{obj.image}/-/resize/x40/-/format/auto/"
            return mark_safe(f'<img src="{url}" style="max-height:40px; border-radius:4px;" />')
        return "No Image"

    image_preview.short_description = "Preview"
