from services.price_checker import PriceCheckerService

service = PriceCheckerService()

# Add a real ASICS product
product_id = service.add_product(
    url="https://outlet.asics.com/pl/pl-pl/fujitrail-packable-jacket/p/2011C991-001.html",
    name="ASICS Fujitrail Packable Jacket",
    scraper_type="asics",
    target_price=150.0
)

print(f"✅ Added product ID: {product_id}")
