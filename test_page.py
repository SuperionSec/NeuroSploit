from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Testing http://localhost:3000...")
    try:
        page.goto('http://localhost:3000', timeout=10000)
        page.wait_for_load_state('networkidle', timeout=10000)
        title = page.title()
        print(f"Title: {title}")
        page.screenshot(path='/workspace/screenshot_3000.png')
        print("Screenshot saved to /workspace/screenshot_3000.png")
    except Exception as e:
        print(f"Error: {e}")

    browser.close()
