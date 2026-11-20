from pages.base_page import BasePage


class CheckoutPage(BasePage):
    PROCEED_CHECKOUT_BTN = "button:has-text('Proceed to Checkout'), button:has-text('Checkout')"
    FIRST_NAME_INPUT = "input[name='firstName']"
    LAST_NAME_INPUT = "input[name='lastName']"
    EMAIL_INPUT = "input[name='email']"
    ADDRESS_INPUT = "input[name='address']"
    CITY_INPUT = "input[name='city']"
    PINCODE_INPUT = "input[name='pinCode']"
    PLACE_ORDER_BTN = "button:has-text('Place Order'), button[type='submit']"

    def proceed_to_checkout(self):
        btn = self.page.locator(self.PROCEED_CHECKOUT_BTN).first
        btn.wait_for(state="visible", timeout=10000)
        btn.click()

    def fill_shipping_and_place_order(self, address: str, city: str, pincode: str, phone: str = ""):
        if self.page.locator(self.FIRST_NAME_INPUT).count() > 0:
            self.fill(self.FIRST_NAME_INPUT, "Test")
        if self.page.locator(self.LAST_NAME_INPUT).count() > 0:
            self.fill(self.LAST_NAME_INPUT, "Student")
        if self.page.locator(self.EMAIL_INPUT).count() > 0:
            self.fill(self.EMAIL_INPUT, "student@example.com")
        self.fill(self.ADDRESS_INPUT, address)
        self.fill(self.CITY_INPUT, city)
        self.fill(self.PINCODE_INPUT, pincode)
        self.click(self.PLACE_ORDER_BTN)
