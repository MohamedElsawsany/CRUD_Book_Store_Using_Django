from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, ISBN

@receiver(post_save, sender=Book)
def create_isbn_for_book(sender, instance, created, **kwargs):
    """
    Signal to automatically create an ISBN object when a book is created
    """
    if created:
        ISBN.objects.create(
            book=instance,
            author=f"Author of {instance.title}",  # You can modify this logic
            title=instance.title
        )