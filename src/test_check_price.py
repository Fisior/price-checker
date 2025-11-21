from services.price_checker import PriceCheckerService

service = PriceCheckerService()

# Check price for product ID 2
print("Checking price...\n")
result = service.check_price(product_id=2)

print("\n--- Result ---")
print(f"Success: {result['success']}")
print(f"Product: {result['product_name']}")
print(f"Price: {result['current_price']} {result['currency']}")
print(f"Checked at: {result['checked_at']}")
