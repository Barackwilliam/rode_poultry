"""
Management command: python manage.py seed_categories
Creates the default product categories with correct slugs if they don't exist.
"""
from django.core.management.base import BaseCommand
from apps.products.models import Category


DEFAULT_CATEGORIES = [
    {'name': 'Day-Old Chicks', 'name_sw': 'Vifaranga vya Siku Moja', 'slug': 'day-old-chicks'},
    {'name': 'Eggs',           'name_sw': 'Mayai',                    'slug': 'eggs'},
    {'name': 'Live Chickens',  'name_sw': 'Kuku Hai',                 'slug': 'live-chickens'},
    {'name': 'Chicken Meat',   'name_sw': 'Nyama ya Kuku',            'slug': 'chicken-meat'},
]


class Command(BaseCommand):
    help = 'Seed default product categories with correct slugs'

    def handle(self, *args, **options):
        created = 0
        for cat_data in DEFAULT_CATEGORIES:
            obj, was_created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'name_sw': cat_data['name_sw'],
                }
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {obj.name}'))
            else:
                self.stdout.write(f'  Already exists: {obj.name}')
        self.stdout.write(self.style.SUCCESS(f'\nDone. {created} categories created.'))
