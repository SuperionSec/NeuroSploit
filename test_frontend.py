from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Test frontend
    print("Testing frontend at http://localhost:3000...")
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')

    title = page.title()
    print(f"Page title: {title}")

    # Take screenshot
    page.screenshot(path='/workspace/frontend_screenshot.png', full_page=True)
    print("Screenshot saved to /workspace/frontend_screenshot.png")

    # Test backend API
    print("\nTesting backend API at http://localhost:8000/api/health...")
    response = page.goto('http://localhost:8000/api/health')
    if response:
        print(f"Status: {response.status}")
        print(f"Body: {response.text()}")

    browser.close()
    print("\nAll tests completed!")
