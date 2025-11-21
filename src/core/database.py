from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    url = Column(String(1000), nullable=False, unique=True)
    name = Column(String(1000), nullable=False)
    target_price = Column(Float, nullable=True)
    scraper_type = Column(String(50), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    price_history = relationship("PriceHistory", back_populates="product")


class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default='PLN')
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    product = relationship("Product", back_populates="price_history")

# Database setup
DATABASE_URL = "sqlite:////app/data/price_checker.db"

def get_engine():
    """Create database engine"""
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows SQL queries
    return engine

def create_tables():
    """Create all tables in the database"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Database tables created!")

def get_session():
    """Get a database session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
