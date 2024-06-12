# E-Commerce API

This is an E-Commerce API built with Django and Django Rest Framework. The API supports functionalities such as product listing, searching, filtering, adding orders to a cart, and calculating the total amount with discounts. It also includes custom error handling for 404 errors.

  -- pip install -r requirements.txt
  -- python manage.py migrate
  -- python manage.py createsuperuser


# API Endpoints
## Products
GET /api/products/: List all products.
GET /api/products/{id}/: Retrieve a single product.
POST /api/products/: Create a new product.
PUT /api/products/{id}/: Update an existing product.
DELETE /api/products/{id}/: Delete a product.

## Categories
GET /api/categories/: List all categories.
POST /api/categories/: Create a new category.

## Cart
GET /api/cart/: Retrieve the authenticated user's cart.
POST /api/cart/: Add orders to the cart.

## Orders
GET /api/orders/: List all orders.
POST /api/orders/: Create a new order.


# Contributing
- Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.
