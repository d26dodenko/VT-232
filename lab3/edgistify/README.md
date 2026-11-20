![CI/CD Quality Gates](https://github.com/BabukhinaVeronika/edgistify-Assignment/actions/workflows/ci.yml/badge.svg)

# E-Commerce Platform

## Overview
This is a full-stack e-commerce platform that allows users to register, log in, add products to their cart, and place orders. The application consists of:
- A **frontend** built with React and TypeScript.
- A **backend** built with Node.js, Express, and MongoDB.
- JWT-based authentication and bcrypt for password hashing.
- **Automated UI/API/Unit Testing & CI/CD Pipeline** with blocking Quality Gates (Playwright, Pytest, Coverage >= 80%, Bandit, Safety).

## Features
### **User Authentication**
- Register a new account with:
  - Full Name
  - Email Address (unique, validated)
  - Password (hashed, minimum 8 characters)
- Login with email and password.
- JWT-based session management.

### **Cart Management**
- Users can add products to their cart (authentication required).
- Each cart item contains:
  - Product ID
  - Quantity (default: 1)
  - User ID
- Product availability is validated before adding.

### **Order Placement**
- Users can place orders with authentication.
- An order includes:
  - User ID
  - List of products with quantity and price
  - Total price
  - Shipping address
  - Payment status (`Pending`, `Paid`, `Failed`)
  - Order status (`Pending`, `Processing`, `Shipped`, `Delivered`)
- The cart is cleared after placing an order.

## Installation & Setup

### Clone the Repository
```sh
git clone [https://github.com/BabukhinaVeronika/edgistify-Assignment.git](https://github.com/BabukhinaVeronika/edgistify-Assignment.git)
cd edgistify-Assignment