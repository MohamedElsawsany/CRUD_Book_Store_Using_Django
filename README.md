# Django Bookstore 📚

A responsive Django-based web application for managing books. Users can add, edit, delete, and view books, each with detailed attributes.

## 🚀 Features

- Add new books
- Edit existing book details
- Delete books
- View list of all books with:
  - Title
  - Author
  - Publication Date
  - Price
- Responsive UI using **Bootstrap**

## 🛠️ Technologies Used

- Python
- Django
- SQLite (default database)
- Bootstrap 5
- HTML / CSS

## 🧪 Setup Instructions

1. **Clone the repository**:
   ```
   git clone https://github.com/MohamedElsawsany/CRUD_Book_Store_Using_Django.git

2. **Create & activate a virtual environment**:
   ```
   python -m venv venv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate

3. **Install dependencies**:
   ```
   pip install -r requirements.txt

4. **Apply migrations**:
   ```
   python bookstore_project\manage.py makemigrations
   python bookstore_project\manage.py migrate
  
5. **Run the development server**:
   ```  
   python manage.py runserver

6. **Access the site**:
   ```
   Open http://localhost:8000 in your browser.

Built with ❤️ using Django and Bootstrap.