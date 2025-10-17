from datetime import datetime

from core.database import create_tables, get_session, Product, PriceHistory

# Create tables
print("Creating database tables...")
create_tables()

# Test adding a product
print("\nTesting database...")
session = get_session()

# Add a test product
product = Product(
    url="https://outlet.asics.com/pl/pl-pl/test-product.html",
    name="Test Jacket",
    target_price=150.00,
    scraper_type="asics"
)

session.add(product)
session.commit()

print(f"✅ Added product: {product.name} (ID: {product.id})")

# Add price history
price = PriceHistory(
    product_id=product.id,
    price=195.00,
    currency="PLN"
)

session.add(price)
session.commit()

print(f"✅ Added price: {price.price} {price.currency}")

session.close()