from django.contrib import admin
from .models import Product, Category
from .forms import ProductAdminForm, CategoryAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['name', 'name_sw', 'slug']
    prepopulated_fields = {'slug': ('name',)}

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
        if obj.image_url:
            url = f"https://ucarecdn.com/{obj.image}/-/resize/x40/-/format/auto/"
            return mark_safe(f'<img src="{url}" style="max-height:40px; border-radius:4px;" />')
        return "No Image"

    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'category', 'price', 'unit', 'stock', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured']
    list_editable = ['price', 'stock', 'is_available', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'name_sw']
    fieldsets = (
        ('English', {'fields': ('name', 'slug', 'description', 'category')}),
        ('Swahili', {'fields': ('name_sw', 'description_sw')}),
        ('Pricing & Stock', {'fields': ('price', 'unit', 'unit_sw', 'stock', 'minimum_order')}),
        ('Images', {'fields': ('image', 'image2', 'image3')}),
        ('Visibility', {'fields': ('is_available', 'is_featured')}),
    )
    def formfield_for_dbfield(self, db_field, **kwargs):
            formfield = super().formfield_for_dbfield(db_field, **kwargs)

            # Orodha ya majina ya picha zako zote nne
            image_fields = ["image", "image2", "image3"]

            if db_field.name in image_fields:
                formfield.widget.attrs.update({
                    "role": "uploadcare-uploader",
                    "data-public-key": "431f160fc3fcf0ffb783",
                    # Unaweza kuongeza hii ili kuruhusu picha tu
                    "data-images-only": "true",
                })

            return formfield

    def image_preview(self, obj):
        html = '<div style="display: flex; gap: 5px;">'
        
        # Tunachukua picha zote kupitia ile property ya 'images' uliyotengeneza kwenye Model
        picha_zilizopo = obj.images # Hii inarudisha list ya URL zenye data
        
        if picha_zilizopo:
            for url in picha_zilizopo:
                # Tunatumia resize ndogo ili zitoshee kwenye mstari mmoja wa Admin
                cdn_url = f"https://ucarecdn.com/{url}/-/resize/x50/-/format/auto/"
                html += f'<img src="{cdn_url}" style="max-height:50px; border-radius:4px; border:1px solid #ddd;" />'
            
            html += '</div>'
            return mark_safe(html)
        
        return "No Images"

    image_preview.short_description = "Galleru Preview"

