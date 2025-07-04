from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.urls import reverse
import uuid

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        unique=True
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(50)
        ]
    )
    description = models.TextField(blank=True)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

class ISBN(models.Model):
    isbn_number = models.CharField(max_length=13, unique=True, editable=False)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='isbn')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.isbn_number:
            self.isbn_number = self.generate_isbn()
        super().save(*args, **kwargs)

    def generate_isbn(self):
        # Generate a simple ISBN-like number
        return f"978{str(uuid.uuid4().int)[:10]}"

    def __str__(self):
        return f"ISBN: {self.isbn_number} - {self.title}"

    class Meta:
        verbose_name = "ISBN"
        verbose_name_plural = "ISBNs"