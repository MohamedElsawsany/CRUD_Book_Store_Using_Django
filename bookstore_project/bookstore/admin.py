from django.contrib import admin
from .models import Book, Category, ISBN

class ISBNInline(admin.StackedInline):
    model = ISBN
    extra = 0
    readonly_fields = ('isbn_number', 'created_at')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'stock_quantity', 'publication_date', 'created_at')
    list_filter = ('categories', 'user', 'publication_date', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'isbn__author')
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ISBNInline]
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'description', 'publication_date', 'price', 'stock_quantity')
        }),
        ('Relationships', {
            'fields': ('user', 'categories')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

@admin.register(ISBN)
class ISBNAdmin(admin.ModelAdmin):
    list_display = ('isbn_number', 'title', 'author', 'book', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('isbn_number', 'title', 'author', 'book__title')
    readonly_fields = ('isbn_number', 'created_at')