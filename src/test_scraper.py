from scrapers.asics_scraper import AsicsScraper

# Create scraper
print("Creating scraper...")
scraper = AsicsScraper(headless=True)

# Test URL
print("Starting price extraction...")
url = "https://outlet.asics.com/pl/pl-pl/sport-run-hood-jacket/p/2011D351-750.html?size=L"

# Get price
result = scraper.get_price(url)

# Print result
print("\n--- Result ---")
print(f"Result dict: {result}")
print(f"Success: {result['success']}")
print(f"Price: {result.get('price', 'NO PRICE')}")

if not result['success']:
    print(f"Error: {result.get('error', 'NO ERROR MESSAGE')}")
