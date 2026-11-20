import json
import os
import sys
from pathlib import Path
import pytest
from playwright.sync_api import Page, Route, expect

QA_ROOT = Path(__file__).resolve().parents[2]
if str(QA_ROOT) not in sys.path:
    sys.path.insert(0, str(QA_ROOT))

from pages.auth_page import AuthPage  # noqa: E402
from pages.catalog_page import CatalogPage  # noqa: E402
from pages.checkout_page import CheckoutPage  # noqa: E402


BASE_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

MOCK_PRODUCTS = [
    {
        "_id": "prod_1",
        "title": "Classic Cotton T-Shirt",
        "price": 45,
        "images": ["https://via.placeholder.com/300"],
        "img1": "https://via.placeholder.com/300",
        "sizes": ["S", "M", "L"],
        "brand": "Clothify",
        "discount": "10%",
        "rating": 4.8,
        "reviews": "124",
        "description": "Soft organic cotton t-shirt",
        "originalPrice": 50,
    },
    {
        "_id": "prod_2",
        "title": "Denim Jacket",
        "price": 95,
        "images": ["https://via.placeholder.com/300"],
        "img1": "https://via.placeholder.com/300",
        "sizes": ["M", "L", "XL"],
        "brand": "Clothify",
        "discount": "15%",
        "rating": 4.6,
        "reviews": "89",
        "description": "Classic fit denim jacket",
        "originalPrice": 110,
    },
]

MOCK_CART = [
    {
        "_id": "cart_1",
        "title": "Classic Cotton T-Shirt",
        "price": 45,
        "quantity": 1,
        "img1": "https://via.placeholder.com/300",
    }
]

MOCK_ORDERS = [
    {
        "_id": "ORD-2026-01",
        "totalPrice": 45,
        "shippingAddress": "123 Main St, Moscow, 101000",
        "paymentStatus": "Pending",
        "orderStatus": "Pending",
        "products": [
            {
                "_id": "item_1",
                "productId": "prod_1",
                "title": "Classic Cotton T-Shirt",
                "img1": "https://via.placeholder.com/300",
                "quantity": 1,
                "price": 45,
            }
        ],
    }
]


@pytest.fixture(autouse=True)
def mock_backend_api(page: Page):
    """Перехват запросов к API (edgistify-assignment.vercel.app/api) для стабильных E2E-тестов."""

    def handle_api(route: Route):
        url = route.request.url.lower()
        method = route.request.method

        if "/users/register" in url:
            route.fulfill(
                status=201,
                content_type="application/json",
                body=json.dumps({"message": "User registered successfully!"}),
            )
        elif "/users/login" in url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(
                    {
                        "token": "mock-jwt-token-2026",
                        "userId": "user_101",
                        "message": "Login successful!",
                    }
                ),
            )
        elif "/products" in url:
            if url.endswith("/products") or "/products?" in url:
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(MOCK_PRODUCTS),
                )
            else:
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(MOCK_PRODUCTS[0]),
                )
        elif "/cart/add" in url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"message": "Product added to cart"}),
            )
        elif "/cart" in url:
            if method == "DELETE":
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps({"message": "Item removed"}),
                )
            else:
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(MOCK_CART),
                )
        elif "/orders/create" in url:
            route.fulfill(
                status=201,
                content_type="application/json",
                body=json.dumps({"message": "Order created", "order": MOCK_ORDERS[0]}),
            )
        elif "/orders/get" in url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(MOCK_ORDERS),
            )
        else:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"ok": True}),
            )

    page.route("**/api/**", handle_api)


def set_authenticated_session(page: Page):
    page.evaluate(
        """() => {
            localStorage.setItem('token', 'mock-jwt-token-2026');
            localStorage.setItem('userId', 'user_101');
        }"""
    )


def test_user_registration(page: Page):
    """Сценарий 1: Регистрация нового пользователя."""
    auth = AuthPage(page, BASE_URL)
    auth.register_user("Test Student", "student@example.com", "StrongPass123!")
    auth.assert_text_visible("User registered successfully!")


def test_user_login(page: Page):
    """Сценарий 2: Вход в систему."""
    auth = AuthPage(page, BASE_URL)
    auth.login_user("student@example.com", "StrongPass123!")
    auth.assert_text_visible("Login successful!")
    expect(page).to_have_url(f"{BASE_URL}/", timeout=5000)


def test_product_search(page: Page):
    """Сценарий 3: Поиск и просмотр товара в каталоге."""
    catalog = CatalogPage(page, BASE_URL)
    catalog.open_catalog()
    catalog.search_product("Classic Cotton T-Shirt")
    catalog.assert_text_visible("Classic Cotton T-Shirt")


def test_add_product_to_cart(page: Page):
    """Сценарий 4: Добавление товара в корзину."""
    set_authenticated_session(page)
    catalog = CatalogPage(page, BASE_URL)
    catalog.open_catalog()
    catalog.open_first_product_and_add_to_cart()
    catalog.assert_text_visible("Product added to cart")


def test_checkout_order(page: Page):
    """Сценарий 5: Оформление заказа."""
    set_authenticated_session(page)
    checkout = CheckoutPage(page, BASE_URL)
    checkout.open_path("/cart")
    checkout.proceed_to_checkout()
    checkout.fill_shipping_and_place_order("123 Main St", "Moscow", "101000")
    checkout.assert_text_visible("Order Placed Successfully!")


def test_user_logout(page: Page):
    """Сценарий 6: Выход из системы."""
    set_authenticated_session(page)
    auth = AuthPage(page, BASE_URL)
    auth.open_path("/products")
    auth.logout_user()
    expect(page).to_have_url(f"{BASE_URL}/login", timeout=5000)
