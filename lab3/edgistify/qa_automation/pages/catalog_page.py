from pages.base_page import BasePage


class CatalogPage(BasePage):
    SEARCH_INPUT = "input[type='search'], input[placeholder*='Search' i]"
    PRODUCT_CARDS = "a[href*='/products/']"
    ADD_TO_CART_BTN = "button:has-text('Add Cart'), button:has-text('Add to Cart')"
    CART_NAV_LINK = "a[href='/cart'], a[href*='cart']"

    def open_catalog(self):
        self.open_path("/products")

    def search_product(self, query: str):
        if self.page.locator(self.SEARCH_INPUT).count() > 0:
            search_box = self.page.locator(self.SEARCH_INPUT).first
            search_box.fill(query)
            search_box.press("Enter")
        else:
            self.page.get_by_text(query, exact=False).first.wait_for(state="visible", timeout=10000)

    def open_first_product_and_add_to_cart(self):
        add_btn = self.page.locator(self.ADD_TO_CART_BTN)
        add_btn.first.wait_for(state="visible", timeout=10000)
        add_btn.first.click()

    def go_to_cart(self):
        self.click(self.CART_NAV_LINK)
