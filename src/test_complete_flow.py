from services.price_checker import PriceCheckerService
from core.database import get_session, Product, PriceHistory

service = PriceCheckerService()

print("=== COMPLETE PRICE CHECKER TEST ===\n")

# 1. Add a real product
print("1. Adding real product...")
product_id = service.add_product(
    url="https://outlet.asics.com/pl/pl-pl/fujitrail-packable-jacket/p/2011C991-001.html",
    name="ASICS Fujitrail Packable Jacket",
    scraper_type="asics",
    target_price=150.0
)
print(f"   ✅ Product added: ID {product_id}\n")

# 2. Check price
print("2. Checking price...")
result = service.check_price(product_id)

if result['success']:
    print(f"   ✅ Price: {result['current_price']} {result['currency']}")
    print(f"   📅 Checked at: {result['checked_at']}\n")
else:
    print(f"   ❌ Failed: {result['error']}\n")

# 3. View price history
print("3. Price history:")
session = get_session()
history = session.query(PriceHistory).filter_by(product_id=product_id).all()

for record in history:
    print(f"   {record.checked_at}: {record.price} {record.currency}")

session.close()

print("\n✅ Test complete!")
