import os
from typing import Generator
import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def base_url() -> str:
    # Vite по умолчанию запускается на http://localhost:5173
    return os.getenv("FRONTEND_URL", "http://localhost:5173")


@pytest.fixture(scope="session")
def api_url() -> str:
    # Express backend (проверьте порт в backend/index.js, обычно 8080 или 5000)
    return os.getenv("BACKEND_URL", "http://localhost:8080")


@pytest.fixture(scope="function")
def page(browser, base_url) -> Generator[Page, None, None]:
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto(base_url)
    yield page
    context.close()
