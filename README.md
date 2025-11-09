# JigsimurHerbal - Django E-commerce Application

A Django-based e-commerce website for herbal products featuring user authentication, product catalog, shopping cart, order management, and admin dashboard.

## 🌿 Features

- **User Management**: Registration, login, profile management, addresses
- **Product Catalog**: Categories, product listing, search, filtering
- **Shopping Cart**: Add to cart, update quantities, cart management
- **Order Processing**: Checkout, order history, order tracking
- **Admin Dashboard**: Product management, order management, user management
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone the repository** (if not already done):

   ```bash
   git clone <your-repo-url>
   cd JigsimurHerbal
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv .venv

   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   - Copy `.env.example` to `.env` (if available)
   - Or create a `.env` file with the following:

   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
JigsimurHerbal/
├── jigsimurherbal/          # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── products/               # Product management app
│   ├── models.py           # Product, Category, Review models
│   ├── views.py            # Product views
│   ├── admin.py            # Admin configuration
│   └── urls.py             # Product URLs
├── users/                  # User management app
│   ├── models.py           # UserProfile, Address models
│   ├── views.py            # User authentication views
│   ├── forms.py            # User forms
│   └── urls.py             # User URLs
├── orders/                 # Order management app
│   ├── models.py           # Cart, Order, OrderItem models
│   ├── views.py            # Cart and checkout views
│   └── urls.py             # Order URLs
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── products/           # Product templates
│   ├── users/              # User templates
│   └── orders/             # Order templates
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
└── manage.py               # Django management script
```

## 🛠️ VS Code Setup

This project includes VS Code configuration:

- **Task**: "Django: Run Server" - Starts the development server
- **Python Environment**: Configured virtual environment
- **Extensions**: Python, Pylance (recommended)

### Running the Server in VS Code

1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type "Tasks: Run Task"
3. Select "Django: Run Server"

Or use the keyboard shortcut `Ctrl+Shift+P` → "Django: Run Server"

## 🎯 Key Applications

### Products App

- **Models**: Product, Category, ProductReview, ProductImage
- **Features**: Product listing, search, filtering, reviews
- **Templates**: Home page, product list, product detail

### Users App

- **Models**: UserProfile, Address
- **Features**: Registration, login, profile management, addresses
- **Templates**: Login, register, profile, address management

### Orders App

- **Models**: Cart, CartItem, Order, OrderItem, ShippingMethod
- **Features**: Shopping cart, checkout, order history
- **Templates**: Cart, checkout, order confirmation

## 🔧 Configuration

### Database

- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

### Static Files

- **Development**: Django serves static files
- **Production**: WhiteNoise for static file serving

### Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated allowed hosts
- `DB_*`: Database configuration (for PostgreSQL)

## 📝 Development Guidelines

### Adding New Features

1. Create models in the appropriate app
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Create views and templates
5. Update URLs
6. Add admin configuration if needed

### Code Style

- Follow Django best practices
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep views simple, move complex logic to models or utils

## 🚀 Deployment

### Production Setup

1. Set `DEBUG=False` in production
2. Configure PostgreSQL database
3. Set up proper static file serving
4. Configure email backend for notifications
5. Set up SSL/HTTPS
6. Configure logging

### Heroku Deployment

1. Add `Procfile`: `web: gunicorn jigsimurherbal.wsgi`
2. Configure environment variables
3. Set up PostgreSQL addon
4. Deploy using Git

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Check the Django documentation: https://docs.djangoproject.com/
- Review the issue tracker for known issues
- Contact the development team

---

**Happy coding! 🌿**
