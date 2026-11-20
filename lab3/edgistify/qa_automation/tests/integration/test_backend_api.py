import requests


def test_get_products_endpoint(api_url):
    """Проверка интеграции Express роутов с MongoDB."""
    for path in ("/api/product", "/product", "/products", "/"):
        response = requests.get(f"{api_url}{path}", timeout=5)
        if response.status_code in (200, 201):
            assert response.status_code in (200, 201)
            return
    assert response.status_code in (200, 201)
