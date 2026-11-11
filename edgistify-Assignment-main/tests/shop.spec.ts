import { test, expect, request } from '@playwright/test';
import { LoginPage, ProductPage, CartPage, CheckoutPage } from '../pages/AppPages';

const uniqueEmail = `testuser${Date.now()}@mail.com`;
const password = 'Password123456789';
const fullName = 'Test User';

test.describe.configure({ mode: 'serial' });

test.describe('E2E тесты интернет-магазина', () => {
    let token: string;
    let userId: string;

    test.beforeAll(async ({ request }) => {
        const registerResponse = await request.post('http://127.0.0.1:5000/api/users/register', {
            data: { fullName, email: uniqueEmail, password }
        });

        if (!registerResponse.ok() && registerResponse.status() !== 400) {
            console.log('Ошибка API при регистрации:', await registerResponse.text());
        }

        const loginResponse = await request.post('http://127.0.0.1:5000/api/users/login', {
            data: { email: uniqueEmail, password }
        });

        if (!loginResponse.ok()) {
            throw new Error(`Бэкенд не пускает. Код: ${loginResponse.status()}. Проверь, запущен ли node index.js.`);
        }

        const body = await loginResponse.json();
        token = body.token;
        userId = body.userId;
    });

    const loginByToken = async (page: any) => {
        await page.goto('/');
        await page.evaluate(({ token, userId }: { token: string, userId: string }) => {
            localStorage.setItem('token', token);
            localStorage.setItem('userId', userId);
        }, { token, userId });
        await page.reload();
    };

    test('1. Регистрация пользователя (через UI)', async ({ page }) => {
        await page.goto('/signup');
        await expect(page.getByPlaceholder('Name')).toBeVisible();
        await expect(page.getByPlaceholder('Email')).toBeVisible();
        await expect(page.getByPlaceholder('Password')).toBeVisible();
        await expect(page.getByRole('button', { name: 'Sign Up' })).toBeVisible();
    });

    test('2. Вход в систему', async ({ page }) => {
        await loginByToken(page);
        await expect(page.getByText(/Logout|Выход/i).first()).toBeVisible({ timeout: 10000 });
    });

    test('3. Поиск товара (проверка каталога)', async ({ page }) => {
        const productPage = new ProductPage(page);
        await productPage.goto();
        await expect(page.locator('.group').first()).toBeVisible({ timeout: 15000 });
    });

    test('4. Добавление товара в корзину (проверка клика)', async ({ page }) => {
        await loginByToken(page);
        const productPage = new ProductPage(page);
        await productPage.goto();

        const firstProduct = page.locator('.group').first();
        await firstProduct.waitFor({ state: 'visible', timeout: 15000 });
        await firstProduct.locator('select').selectOption({ index: 0 });
        await firstProduct.getByRole('button', { name: /Add Cart|Добавить/i }).click();
        await expect(page.locator('.Toastify__toast')).toBeVisible({ timeout: 5000 });
    });

    test('5. Оформление заказа (проверка страницы)', async ({ page }) => {
        await loginByToken(page);
        await page.goto('/placed');
        await expect(page.getByText(/Order Placed Successfully!/i)).toBeVisible({ timeout: 15000 });
    });

    test('6. Выход из системы', async ({ page }) => {
        await loginByToken(page);
        await expect(page.getByText(/Logout|Выход/i).first()).toBeVisible();
        await page.getByText(/Logout|Выход/i).first().click();
        await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible({ timeout: 10000 });
    });
});