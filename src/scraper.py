from playwright.sync_api import sync_playwright

url = "https://outlet.asics.com/pl/pl-pl/fujitrail-packable-jacket/p/2011C991-001.html"

print(f"Scraping: {url}\n")

try:
    with sync_playwright() as p:
        # Launch with more realistic settings
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # Create page with realistic viewport
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        print("📄 Loading page...")
        
        # Load page with timeout
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        
        # Wait for JavaScript to load
        page.wait_for_timeout(3000)
        
        print("✅ Page loaded!")
        print(f"📋 Title: {page.title()}")
        
        # Extract the price
        print("\n💰 Extracting price...")
        
        try:
            # Find element by class name
            price_element = page.locator("span.price-sales")
            
            # Get the text content
            price_text = price_element.text_content()
            
            # Clean it up (remove whitespace)
            price_clean = price_text.strip()
            
            print(f"✅ Price found: {price_clean}")
            
        except Exception as e:
            print(f"❌ Could not find price: {e}")
        
        browser.close()
        
except Exception as e:
    print(f"❌ Error: {e}")