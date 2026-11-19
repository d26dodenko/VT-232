![CI Pipeline](https://github.com/d26dodenko/VT-232/actions/workflows/ci.yml/badge.svg?branch=Zhavoronkova_Darya_03)
# E-Commerce Platform

## Overview
This is a full-stack e-commerce platform that allows users to register, log in, add products to their cart, and place orders. The application consists of:
- A **frontend** built with React and TypeScript.
- A **backend** built with Node.js, Express, and MongoDB.
- JWT-based authentication and bcrypt for password hashing.

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
git clone https://github.com/Sajid788/edgistify-Assignment.git
cd backend
cd frontend
```

### Backend Setup
```sh
cd backend
npm install
nodemon index.js
```

### Frontend Setup
```sh
cd frontend
npm install
npm run dev
```


## Project Structure
### **Backend (`backend/` directory)**
```
backend/
├── config/
│   ├── db.js  # MongoDB connection setup
│
├── controllers/
│   ├── CartController.js
│   ├── OrderController.js
│   ├── ProductController.js
│   ├── UserController.js
│
├── middleware/
│   ├── authentication.js # JWT verification middleware
│
├── models/
│   ├── CartModel.js
│   ├── OrderModel.js
│   ├── ProductModel.js
│   ├── UserModel.js
│
├── routes/
│   ├── CartRoutes.js
│   ├── OrderRoutes.js
│   ├── ProductRoutes.js
│   ├── UserRoutes.js
│
├── .env  # Environment variables
├── index.js  # Main server file
```

### **Frontend (`frontend/src/` directory)**
```
frontend/src/
├── api/
│   ├── api.ts  # Handles API requests
│
├── components/
│   ├── Navbar.tsx  # Navigation bar
│
├── pages/
│   ├── Cart.tsx
│   ├── Checkout.tsx
│   ├── Login.tsx
│   ├── PlacedOrder.tsx
│   ├── Product.tsx
│   ├── ProductDetails.tsx
│   ├── Signup.tsx
│
├── routes/
│   ├── index.tsx  # Defines routes
│
├── App.tsx  # Main App component
├── main.tsx  # Application entry point
```

## Installation
### **Prerequisites**
- Node.js & npm
- MongoDB

### **Backend Setup**
```bash
cd backend
npm install
npm start  # Runs the backend server
```

### **Frontend Setup**
```bash
cd frontend
npm install
npm run dev  # Runs the frontend development server
```

## API Endpoints
### **User Authentication**
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - User login

### **Cart Management**
- `POST /api/cart/add` - Add product to cart (authentication required)
- `GET /api/cart/` - Get user's cart items
- `DELETE /api/cart/:id` - Remove item from cart

### **Order Management**
- `POST /api/orders/place` - Place an order
- `GET /api/orders/` - Get user's order history

## Technologies Used
- **Frontend:** React, TypeScript, Axios
- **Backend:** Node.js, Express, MongoDB, Mongoose
- **Authentication:** JWT, bcrypt.js
- **Styling:** CSS, Tailwind (if used)

## Future Enhancements
- Implement payment gateway integration (e.g., Stripe, PayPal)
- Add admin panel for managing products and orders
- Improve UI/UX with animations and better styling

## License
This project is licensed under the MIT License

## 📌 Application ScreenShots
![Screenshot 2025-02-12 190804](https://github.com/user-attachments/assets/9fbbffab-1896-4b8a-8b3c-77c0bf7f53f3)
![image](https://github.com/user-attachments/assets/6ce8da37-acef-4a47-a473-12d67ef8a9ec)
![image](https://github.com/user-attachments/assets/1cb4b815-995f-4ad2-96b6-419cfebb3730)
![image](https://github.com/user-attachments/assets/5ee849cf-2452-46de-87e4-dae16bd46706)
![image](https://github.com/user-attachments/assets/72b51071-49d6-456b-a05f-f092d1533ebb)
![image](https://github.com/user-attachments/assets/18d30e55-9616-4bc2-9fa9-e24c6b50cc9b)
![image](https://github.com/user-attachments/assets/53e0fbbe-78b3-40fc-849d-ab8b67b37b6e)









