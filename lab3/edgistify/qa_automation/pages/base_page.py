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
