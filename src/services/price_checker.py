from core.database import Product, PriceHistory, get_session
from core.scraper_factory import ScraperFactory
import logging

class PriceCheckerService:
    """Service to manage products and price checking"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def add_product(self, url: str, name: str, scraper_type: str, target_price: float = None):
        """Add a new product to monitor"""
        session = get_session()
        
        try:
            product = Product(
                url=url,
                name=name,
                scraper_type=scraper_type,
                target_price=target_price
            )
            
            session.add(product)
            session.commit()
            
            self.logger.info(f"Added product: {product.name} (ID: {product.id})")
            
            return product.id
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error adding product: {e}")
            raise
            
        finally:
            session.close()

    def check_price(self, product_id: int):
        """
        Check current price for a product and save to history
        
        Args:
            product_id: ID of product to check
            
        Returns:
            dict with price info
        """
        session = get_session()
    
        try:
            # 1. Get product from database
            product = session.query(Product).get(product_id)
            
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            self.logger.info(f"Checking price for: {product.name}")
            
            # 2. Get the right scraper
            scraper = ScraperFactory.get_scraper(product.scraper_type)
            
            # 3. Scrape the price
            result = scraper.get_price(product.url)
            
            if not result['success']:
                self.logger.error(f"Failed to get price: {result.get('error')}")
                return result
            
            if not result['success']:
                error_msg = result.get('error', 'Unknown error')

                if 'Timeout' in error_msg:
                    self.logger.warning(f"Product page timeout: {product.name}")
                elif '404' in error_msg:
                    self.logger.warning(f"Product not found (404): {product.name}")
                    # Maybe mark product as inactive?
                    product.active = False
                    session.commit()
                else:
                    self.logger.error(f"Failed to get price: {error_msg}")

                return {
                    'success': False,
                    'error': error_msg,
                    'product_name': product.name
                }
            
            # 4. Save to price_history
            price_history = PriceHistory(
                product_id=product.id,
                price=float(result['price'].replace(',', '.').split()[0]),  # Clean price
                currency=result.get('currency', 'PLN')
            )
            
            session.add(price_history)
            session.commit()
            
            self.logger.info(f"Price saved: {price_history.price} {price_history.currency}")
            
            return {
                'success': True,
                'product_name': product.name,
                'current_price': price_history.price,
                'currency': price_history.currency,
                'checked_at': price_history.checked_at
            }
            
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error checking price: {e}")
            raise
            
        finally:
            session.close()