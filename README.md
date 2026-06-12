# Grocery Backend API

Django REST API backend for the Grocery application.

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

Update the following variables in `.env`:
- `DJANGO_SECRET_KEY`: Generate a secret key for production
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Add your domain names
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Database configuration
- `CORS_ALLOWED_ORIGINS`: Add your frontend domain

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/` - Get current user profile
- `PUT /api/auth/` - Update user profile
- `DELETE /api/auth/` - Delete user account
- `POST /api/auth/reset-password/` - Reset password

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create category (Admin)
- `GET /api/categories/:id/` - Get category by ID
- `PUT /api/categories/:id/` - Update category (Admin)
- `DELETE /api/categories/:id/` - Delete category (Admin)

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create product (Admin)
- `GET /api/products/:id/` - Get product by ID
- `PUT /api/products/:id/` - Update product (Admin)
- `DELETE /api/products/:id/` - Delete product (Admin)
- `GET /api/products/search/` - Search products

### Cart
- `GET /api/cart/` - Get user's cart
- `POST /api/cart/add/` - Add item to cart
- `PUT /api/cart/:id/` - Update cart item
- `DELETE /api/cart/:id/` - Remove cart item
- `DELETE /api/cart/clear/` - Clear cart

### Orders
- `POST /api/orders/create/` - Create order from cart
- `GET /api/orders/` - Get current user's orders
- `GET /api/orders/:id/` - Get order by ID
- `GET /api/orders/admin/all/` - Get all orders (Admin)
- `PATCH /api/orders/admin/:id/status/` - Update order status (Admin)

### Admin
- `GET /api/admin/dashboard/` - Get dashboard statistics (Admin)
- `GET /api/admin/users/` - Get all users (Admin)
- `PATCH /api/admin/users/:id/` - Toggle user status (Admin)

## Deployment

### Render/Railway
1. Push this repository to GitHub
2. Connect to Render/Railway
3. Configure environment variables
4. Deploy

The `Procfile` is included for deployment:
```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

## API Documentation
Swagger UI: `http://localhost:8000/api/docs/`
ReDoc: `http://localhost:8000/api/redoc/`
