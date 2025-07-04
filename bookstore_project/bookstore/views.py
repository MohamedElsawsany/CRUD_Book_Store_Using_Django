from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Book, Category, ISBN
from .forms import BookForm, CategoryForm, CustomUserCreationForm

# Authentication Views
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('book_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Book Views
class BookListView(ListView):
    model = Book
    template_name = 'bookstore/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.select_related('user', 'isbn').prefetch_related('categories')
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(isbn__author__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(categories__id=category)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['current_query'] = self.request.GET.get('q', '')
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'bookstore/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.select_related('user', 'isbn').prefetch_related('categories')

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'bookstore/book_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'bookstore/book_form.html'

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)

class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'bookstore/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookstore.delete_book'

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Category Views
@login_required
@permission_required('bookstore.add_category', raise_exception=True)
def category_create_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('book_list')
    else:
        form = CategoryForm()
    return render(request, 'bookstore/category_form.html', {'form': form})

# Function-based views for demonstration
@login_required
def my_books_view(request):
    books = Book.objects.filter(user=request.user).select_related('isbn').prefetch_related('categories')
    return render(request, 'bookstore/my_books.html', {'books': books})