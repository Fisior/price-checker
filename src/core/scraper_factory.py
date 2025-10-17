from scrapers.asics_scraper import AsicsScraper

class ScraperFactory:
    """Factory class to create scraper instances based on type"""

    SCRAPERS = {
        "asics": AsicsScraper,
    }

    @staticmethod
    def get_scraper(scraper_type: str):
        """
        Get scraper instance based on type
        
        Args:
            scraper_type: Type of scraper (asics, zalando, etc.)
            
        Returns:
            Scraper instance
            
        Raises:
            ValueError: If scraper type is unknown
        """
        scraper_type_lower = scraper_type.lower()
        scraper_class = ScraperFactory.SCRAPERS.get(scraper_type_lower)

        if not scraper_class:
            available = ', '.join(ScraperFactory.SCRAPERS.keys())
            raise ValueError(f"Unknown scraper '{scraper_type}'. Available: {available}")
        
        return scraper_class()
