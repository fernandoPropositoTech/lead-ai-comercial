from playwright.sync_api import sync_playwright


def render_page(url):

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )

            html = page.content()

            browser.close()

            return html

    except Exception as e:

        print(
            f"Erro Playwright: {e}"
        )

        return None