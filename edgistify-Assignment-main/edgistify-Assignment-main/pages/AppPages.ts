import { Page, expect } from '@playwright/test';

export class LoginPage {
    constructor(private page: Page) {}
    async goto() { await this.page.goto('/login'); }
}

export class ProductPage {
    constructor(private page: Page) {}
    async goto() { await this.page.goto('/products'); }
}

export class CartPage {
    constructor(private page: Page) {}
    async goto() { await this.page.goto('/cart'); }

    async proceedToCheckout() {
        await this.page.getByRole('button', { name: /Proceed to Checkout/i }).click();
    }
}

export class CheckoutPage {
    constructor(private page: Page) {}

    async fillShipping(address: string, city: string, zip: string) {
        await this.page.locator('input[name="firstName"]').fill('Test');
        await this.page.locator('input[name="lastName"]').fill('User');
        await this.page.locator('input[name="email"]').fill('test@example.com');
        await this.page.locator('input[name="address"]').fill(address);
        await this.page.locator('input[name="city"]').fill(city);
        await this.page.locator('input[name="pinCode"]').fill(zip);
    }

    async placeOrder() {
        await this.page.getByRole('button', { name: 'Place Order' }).click();
    }

    async expectSuccess() {
        await expect(this.page.getByText('Order Placed Successfully!')).toBeVisible({ timeout: 10000 });
    }
}