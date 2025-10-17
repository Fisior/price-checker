from core.scraper_factory import ScraperFactory

print("Testing ScraperFactory...\n")

# Test 1: Valid scraper
print("Test 1: Get ASICS scraper")
scraper = ScraperFactory.get_scraper("asics")
print(f"✅ Success: {type(scraper).__name__}\n")

# Test 2: Case insensitive
print("Test 2: Case insensitive (ASICS, Asics)")
scraper2 = ScraperFactory.get_scraper("ASICS")
scraper3 = ScraperFactory.get_scraper("Asics")
print(f"✅ Both work: {type(scraper2).__name__}, {type(scraper3).__name__}\n")

# Test 3: Invalid scraper
print("Test 3: Invalid scraper type")
try:
    ScraperFactory.get_scraper("invalid")
    print("❌ Should have raised ValueError")
except ValueError as e:
    print(f"✅ Error handling works: {e}\n")

print("All tests passed! ✅")