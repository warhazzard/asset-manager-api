from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum as SQLEnum 
from sqlalchemy.sql import func
from app.database import Base 
from enum import Enum 


class Category(str, Enum):
    IT_EQUIPMENTS = "IT Equipments"
    FURNITURE = "Furniture"
    SOFTWARE_LICENSES = "Software Licenses"


class AssetStatus(str, Enum):
    AVAILABLE = "Available"
    ASSIGNED = "Assigned"
    UNDER_MAINTENANCE = "Under Maintenance"
    RETIRED = "Retired"


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(SQLEnum(Category), nullable=False)
    status = Column(SQLEnum(AssetStatus), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    serial_number = Column(String(100), nullable=True)
    purchase_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=func.now())
