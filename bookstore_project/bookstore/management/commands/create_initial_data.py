from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from bookstore.models import Category, Book

class Command(BaseCommand):
    help = 'Create initial data for the bookstore'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Fiction', 'description': 'Fictional books and novels'},
            {'name': 'Non-Fiction', 'description': 'Non-fictional books and educational content'},
            {'name': 'Science', 'description': 'Scientific books and research'},
            {'name': 'Technology', 'description': 'Technology and programming books'},
            {'name': 'History', 'description': 'Historical books and biographies'},
            {'name': 'Mystery', 'description': 'Mystery and thriller books'},
            {'name': 'Romance', 'description': 'Romance novels'},
            {'name': 'Fantasy', 'description': 'Fantasy and magical realism'},
        ]
        
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
        
        # Create a superuser if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@bookstore.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Created superuser: admin/admin123')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Initial data created successfully!')
        )