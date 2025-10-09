from scrapers.base_scraper import BaseScraper

class AsicsScraper(BaseScraper):
    """Scraper for ASICS Outlet website"""

    # def _extract_price(self) -> str:
    #     """Get price from ASICS product page"""
    #     price_element = self.page.locator("span.price-sales")
    #     price_text = price_element.text_content()
    #     clean_price = self._clean_price(price_text=price_text)
    #     return clean_price
    
    def _extract_price(self) -> str:
        """Get price from ASICS product page"""
        self.logger.info("Attempting to extract price...")
        
        price_element = self.page.locator("span.price-sales")
        
        # Check if element exists
        count = price_element.count()
        self.logger.info(f"Found {count} price elements")
        
        if count == 0:
            self.logger.warning("No price element found! Checking page content...")
            # Let's see what's on the page
            self.logger.info(f"Page title: {self.page.title()}")
        
        price_text = price_element.text_content()
        self.logger.info(f"Raw price text: '{price_text}'")
        
        clean_price = self._clean_price(price_text)
        self.logger.info(f"Clean price: '{clean_price}'")
        
        return clean_price
