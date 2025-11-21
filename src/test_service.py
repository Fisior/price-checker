from services.price_checker import PriceCheckerService

print("Testing PriceCheckerService...\n")

service = PriceCheckerService()

# Add a test product
product_id = service.add_product(
    url="https://outlet.asics.com/pl/pl-pl/test-jacket.html",
    name="Test ASICS Jacket",
    scraper_type="asics",
    target_price=150.0
)

print(f"\n✅ Product added with ID: {product_id}")
