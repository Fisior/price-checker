from core.database import get_session, Product

session = get_session()

# Get all products
products = session.query(Product).all()

print(f"Total products in database: {len(products)}\n")

for product in products:
    print(f"ID: {product.id}")
    print(f"Name: {product.name}")
    print(f"URL: {product.url}")
    print(f"Scraper: {product.scraper_type}")
    print(f"Target Price: {product.target_price}")
    print(f"Created: {product.created_at}")
    print("-" * 50)

session.close()
