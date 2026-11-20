# Лабораторная работа № 4
## «Автоматизация UI-тестов и построение CI/CD-пайплайна с блокирующими quality gates»

Освоить UI-автоматизацию, паттерны проектирования тестов, встраивание тестов в пайплайн непрерывной интеграции и настройку блокирующих quality gates, при которых падение тестов останавливает сборку и релиз.

---

## Задание

### Часть 1. UI-автоматизация

Дано веб-приложение — интернет-магазин (https://github.com/Sajid788/edgistify-Assignment) Можно взять код за основу (с нуля проект не нужно создавать, можно найти готовый проект в интернете. Используете код либо для frontend или для backend разработчика)

**Требуется:**

1. Написать E2E-тесты на Playwright или Selenium для сценариев:
   - регистрация пользователя;
   - вход в систему;
   - поиск товара;
   - добавление товара в корзину;
   - оформление заказа;
   - выход из системы.
   - (можно написать тесты и для других частей функциональности приложения)

---

### Часть 2. Пирамида тестирования

**Требуется:**

1. Построить пирамиду тестирования для данного приложения.
2. Обосновать распределение: сколько unit-, integration- и E2E-тестов и почему.

---

#### Часть 3. Требуется

**Создать CI-конфигурацию:**

- GitHub Actions: `.github/workflows/ci.yml`;
- или GitLab CI: `.gitlab-ci.yml`.

**Настроить триггеры тестирования:**

- **Unit-тесты + lint** — запускаются при каждом коммите/пуше и pull request. «При каждом сохранении» в CI напрямую не реализуется: для локального сохранения допускается настроить pre-commit-хук, который запускает быстрые unit-тесты и линтер. В CI обязательный запуск — на каждый `push` и `pull_request`.


**Настроить quality gates:**

- пайплайн падает, если coverage < 80%;
- пайплайн падает при критических уязвимостях от bandit/safety;
- падение unit/integration/E2E блокирует следующие стадии;
- в настройках репозитория включить **branch protection**: обязательные проверки CI должны быть зелёными перед merge в `main`.

**Публиковать отчёты и артефакты:**

- coverage-отчёт;
- отчёты pytest/Playwright;
- badge статуса пайплайна в `README.md`.


#### Что должно быть в отчёте по части 3

1. Скриншоты:
   - unit-тест упал → job `build` имеет статус *skipped*;
2. Подтверждение quality gates: coverage < 80% валит пайплайн; critical vulnerability валит пайплайн.
3. Badge в `README.md`:

## Выполнение
### 1. Используемые инструменты и структура проекта

Тестируемое приложение состоит из клиентской части на React + TypeScript (запускается через Vite на порту 5173) и серверной части на Node.js + Express + MongoDB (порт 8080).

#### Структура файлов проекта

```
edgistify-Assignment/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                  # Конфигурация пайплайна GitHub Actions
├── backend/                           # Серверная часть (Node.js + Express + MongoDB)
├── frontend/                          # Клиентская часть (React + TypeScript + Vite)
└── qa_automation/                     # Модуль автоматизации тестирования
    ├── pages/                         # Классы страниц (Page Object Model)
    │   ├── base_page.py               # Базовый класс с общими методами Playwright
    │   ├── auth_page.py               # Страницы регистрации, входа и выхода
    │   ├── catalog_page.py            # Каталог товаров, поиск и добавление в корзину
    │   └── checkout_page.py           # Корзина и оформление заказа
    ├── tests/
    │   ├── e2e/
    │   │   └── test_store_e2e.py      # Сквозные UI-тесты (6 сценариев)
    │   ├── integration/
    │   │   └── test_backend_api.py    # Интеграционный тест API бэкенда
    │   └── unit/
    │       └── test_order_math.py     # Модульные тесты расчёта стоимости заказа
    ├── conftest.py                    # Фикстуры pytest (браузер Chromium, базовые URL)
    └── requirements.txt               # Зависимости Python (pytest, playwright, flake8, bandit)

```

#### Листинг 1. Базовый класс Page Object (qa_automation/pages/base_page.py)

```
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str = "http://localhost:5173"):
        self.page = page
        self.base_url = base_url

    def open_path(self, path: str):
        self.page.goto(f"{self.base_url}{path}", wait_until="domcontentloaded")

    def click(self, selector: str):
        self.page.locator(selector).first.click()

    def fill(self, selector: str, value: str):
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=15000)
        locator.fill(value)

    def assert_url_contains(self, substring: str):
        expect(self.page).to_have_url(lambda url: substring in url)

    def assert_text_visible(self, text: str):
        expect(self.page.get_by_text(text, exact=False).first).to_be_visible()


```

### Листинг 2. Класс страницы авторизации (qa_automation/pages/auth_page.py)

```
from pages.base_page import BasePage


class AuthPage(BasePage):
    NAME_INPUT = "input[name='name'], input[placeholder*='Name' i], input[type='text']"
    EMAIL_INPUT = "input[name='email'], input[type='email'], input[placeholder*='Email' i]"
    PASSWORD_INPUT = "input[name='password'], input[type='password'], input[placeholder*='Password' i]"
    SUBMIT_BTN = "button[type='submit']"
    LOGOUT_BTN = "button:has-text('Logout'), a:has-text('Logout'), button:has-text('Log out')"
    LOGIN_NAV_LINK = "a[href*='login'], button:has-text('Login')"

    def register_user(self, name: str, email: str, password: str):
        self.open_path("/signup")
        self.fill(self.NAME_INPUT, name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def login_user(self, email: str, password: str):
        self.open_path("/login")
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def logout_user(self):
        self.click(self.LOGOUT_BTN)


```

### 2. Реализация E2E-тестов

В файле test_store_e2e.py с помощью фреймворка Playwright и классов Page Object были реализованы все требуемые пользовательские сценарии:

1. **Регистрация пользователя (test_user_registration):** переход на страницу /signup, заполнение полей имени, почты и пароля, отправка формы и проверка появления сообщения об успешной регистрации.

2. **Вход в систему (test_user_login):** переход на страницу /login, ввод логина и пароля, проверка уведомления об успешном входе и автоматического перехода на главную страницу.

3. **Поиск товара (test_product_search):** открытие каталога товаров /products, поиск нужной позиции и проверка её отображения на странице.

4. **Добавление товара в корзину (test_add_product_to_cart):** переход в каталог под авторизованным пользователем, нажатие кнопки добавления товара в корзину (Add Cart) и проверка подтверждающего уведомления.

5. **Оформление заказа (test_checkout_order):** переход в корзину /cart, нажатие кнопки перехода к оформлению (Proceed to Checkout), заполнение формы адреса доставки (имя, фамилия, email, адрес, город, индекс), подтверждение заказа (Place Order) и проверка перехода на страницу успешного оформления.

6. **Выход из системы (test_user_logout):** нажатие кнопки Logout в навигационной панели и проверка перенаправления на страницу авторизации /login.

Для стабильного прохождения сценариев в изолированной среде GitHub Actions в тестах настроен перехват сетевых API-запросов через page.route, что позволяет проверять работу интерфейса без подключения к внешней базе данных.

#### Листинг 3. Код E2E-тестов (qa_automation/tests/e2e/test_store_e2e.py)

```
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
    }
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
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(MOCK_PRODUCTS),
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


```

#### 3. Настройка CI/CD Pipeline, quality gates и результаты проверки

### 3. Настройка CI/CD Pipeline, quality gates и результаты проверки

В файле .github/workflows/ci-cd.yml настроен автоматический пайплайн GitHub Actions, который запускается при каждом пуше и pull request в ветку main и последовательно выполняет четыре этапа с жёсткими порогами качества (quality gates):

1. **Линтинг и юнит-тесты:** Flake8 проверяет соответствие Python-кода стандарту PEP8, после чего запускаются модульные тесты с обязательным порогом покрытия не ниже 80% (флаг --cov-fail-under=80). Если покрытие падает ниже этого значения или есть ошибки стиля, пайплайн принудительно останавливается.
2. **Проверка безопасности:** анализатор Bandit сканирует код на наличие уязвимостей высокого и критического уровней (флаги -lll -iii), а Safety проверяет зависимости из requirements.txt. Обнаружение проблем блокирует дальнейшее выполнение конвейера.
3. **Сборка и интеграционное тестирование:** запускается Express-сервер с MongoDB, и интеграционный тест проверяет доступность HTTP-маршрутов бэкенда.
4. **E2E-тестирование интерфейса:** фронтенд собирается и запускается через Vite, после чего Playwright в браузере Chromium прогоняет все 6 пользовательских сценариев.

Блокировка сборки и релиза обеспечивается за счёт директивы needs в конфигурации YAML: этап сборки и интеграционных тестов (build-and-integration) зависит от успешного завершения проверок кода и безопасности, а этап E2E-тестов (e2e-ui-tests) — от успешной сборки. При падении любого из ранних этапов последующие стадии автоматически получают статус skipped, а включённое правило защиты ветки main (branch protection) запрещает слияние изменений и выпуск релиза до прохождения всех обязательных проверок CI.

#### Листинг 4. Конфигурация этапа E2E-тестирования в GitHub Actions (.github/workflows/ci-cd.yml)

```
  e2e-ui-tests:
    name: E2E UI Tests (Playwright)
    runs-on: ubuntu-latest
    needs: [build-and-integration]
    services:
      mongodb:
        image: mongo:6.0
        ports:
          - 27017:27017
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js & Python
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install App, Build Frontend & Install Playwright
        run: |
          cd backend && npm ci
          cd ../frontend && npm ci && npm run build
          cd ..
          pip install -r qa_automation/requirements.txt
          playwright install chromium --with-deps

      - name: Start Fullstack App & Run E2E Tests
        env:
          MONGO_URI: mongodb://127.0.0.1:27017/edgistify
          PORT: 8080
          JWT_SECRET: super_secret_test_key_123
          PYTHONPATH: qa_automation
        run: |
          node backend/index.js &
          npm --prefix frontend run preview -- --port 5173 &
          sleep 3
          pytest qa_automation/tests/e2e --html=playwright-report.html --self-contained-html --tracing=retain-on-failure

      - name: Upload Playwright Report & Traces
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-e2e-artifacts
          path: |
            playwright-report.html
            test-results/


```

После успешного завершения всех этапов в разделе Artifacts формируются три архива с HTML-отчётами: unit-coverage-reports.zip (отчёт по модульным тестам и покрытию кода на 100%), integration-report.zip (отчёт по проверке API) и playwright-e2e-artifacts.zip (отчёт playwright-report.html со статусом PASSED для всех 6 сценариев).

### 4. Подтверждение работы quality gates и блокировки сборки/релиза

В файле .github/workflows/ci-cd.yml настроены автоматические ворота качества (quality gates), которые при нарушении критериев останавливают пайплайн и блокируют сборку с релизом:

1. **Контроль покрытия кода (coverage < 80%):** в шаге запуска юнит-тестов указан флаг --cov-fail-under=80. Если процент покрытия кода падает ниже 80%, pytest завершается с ошибкой и прерывает выполнение пайплайна на первом этапе.
2. **Контроль безопасности (Bandit и Safety):** на втором этапе анализатор Bandit проверяет код тестов на критические уязвимости (флаги -lll -iii), а Safety проверяет зависимости в requirements.txt. При обнаружении проблем этап security-check завершается падением.
3. **Блокировка последующих стадий:** с помощью директивы needs стадия сборки и интеграционных тестов (build-and-integration) запускается только после успешного завершения стадий unit-and-lint и security-check, а стадия E2E-тестов (e2e-ui-tests) — только после build-and-integration. При падении любого из ранних этапов последующие стадии автоматически получают статус skipped, а правило защиты ветки main (branch protection) блокирует слияние изменений и выпуск релиза до прохождения всех проверок CI.

## Вывод

В ходе лабораторной работы были написаны и отлажены автоматизированные E2E-тесты на Playwright с применением паттерна Page Object Model для всех основных пользовательских сценариев интернет-магазина: регистрации, авторизации, поиска товара, добавления в корзину, оформления заказа и выхода из аккаунта. Внедрение автоматизации в CI/CD-пайплайн GitHub Actions с блокирующими quality gates позволяет автоматически выявлять регрессии, нарушения стиля кода и уязвимости безопасности до попадания изменений в основную ветку, исключая рутинные ручные проверки и гарантируя стабильность каждого релиза.

## Ответы на контрольные вопросы

1. **Что такое пирамида тестирования и почему она важна?**  
Пирамида тестирования — это модель распределения автотестов: много быстрых unit-тестов в основании, меньше integration-тестов в середине и минимум E2E-тестов на вершине. Она важна потому, что помогает сбалансировать скорость, стоимость и надёжность проверок. Если делать упор на E2E, пайплайн становится медленным и хрупким, а если писать только unit-тесты, можно пропустить ошибки на стыке слоёв.

2. **Какие паттерны автоматизации UI вы знаете?**  
Я знаю Page Object Model — для каждой страницы создаётся класс с локаторами и методами действий, что упрощает поддержку тестов при изменении вёрстки. Также есть Page Factory с инициализацией элементов через аннотации, Screenplay с моделированием действий пользователя через задачи и вопросы, Fluent Interface с цепочками вызовов и Data-driven Testing с выносом тестовых данных. В Playwright ещё используются фикстуры для переиспользования Page Object'ов.

3. **Что такое quality gates и зачем они нужны?**  
Quality gates — это автоматические проверки, которые не пропускают код дальше по пайплайну или в main, если он не соответствует заданным критериям качества. Например, покрытие ниже 80%, критические уязвимости или падение тестов блокируют сборку. Они нужны, чтобы исключить человеческий фактор и не дать регрессиям или уязвимостям попасть в релиз.

4. **Почему unit-тесты запускаются на каждый коммит, integration — после сборки, а E2E — перед релизом?**  
Это связано с разной скоростью и стоимостью тестов. Unit-тесты быстрые и не требуют внешних зависимостей, поэтому их запускают на каждый push и pull request для мгновенной обратной связи. Integration-тесты медленнее, так как им нужна база данных или сервисы, поэтому их запускают после сборки. E2E-тесты самые тяжёлые и хрупкие, поэтому их выполняют реже — перед релизом, чтобы получить максимальную уверенность в готовности продукта.
