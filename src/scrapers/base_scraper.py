import logging
from typing import Optional
from abc import ABC, abstractmethod

from playwright.sync_api import sync_playwright, Page, Browser

class BaseScraper(ABC):
    """Base class for all scrapers with shared browser logic"""

    def __init__(self, headless=True, timeout=60000):
        self.headless = headless
        self.timeout = timeout
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for this scraper"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _setup_browser(self):
        """Setup browser with common configuration"""
        self.logger.info("Setting up browser...")

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )

        context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        self.page = context.new_page()
        self.logger.info("Browser setup complete")

    def _load_page(self, url: str):
        """Load a page with common settings"""
        if not self.page:
            raise Exception("Browser not setup. Call _setup_browser() first")
        
        self.logger.info(f"oading page: {url}")
        self.page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
        self.page.wait_for_timeout(3000)
        self.logger.info("Page loaded successfully")

    def _close_browser(self):
        if self.browser:
            self.browser.close()

    def _clean_price(self, price_text: str) -> str:
        """Clean price text"""
        return price_text.strip()
    
    @abstractmethod
    def _extract_price(self) -> str:
        """Each scraper implements its own price extraction logic"""
        pass
    
    def get_price(self, url: str) -> dict:
        """Main method to get price from URL"""
        try:
            self._setup_browser()
            self._load_page(url=url)
            price = self._extract_price()
            return self._format_success(url=url, price=price)
          
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return self._format_error(error=e, url=url)
        
        finally:
            self._close_browser()

    def _format_success(self, price: str, url: str) -> dict:
        """Format successful result"""
        return {
            "price": price,
            "success": True,
            "url": url,
            "currency": "PLN"
        }
    
    def _format_error(self, error: Exception, url: str) -> dict:
        """Format error result"""
        return {
            "price": None,
            "success": False,
            "error": str(error),
            "url": url
        }