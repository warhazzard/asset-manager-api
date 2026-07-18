from pydantic import BaseModel, Field, ConfigDict 
from typing import Optional
from datetime import datetime, date
from app.models.asset import Category, AssetStatus 


class AssetBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Name of the asset")
    category: Category = Field(description="Category Asset belongs to")
    serial_number: Optional[str] = Field(default=None, max_length=100, description="Serial number of the asset")
    status: AssetStatus = Field(description="Status of the Asset")
    assigned_to: Optional[int] = Field(default=None, description="ID of the user the asset is assigned to")
    purchase_date: Optional[date] = Field(default=None, description="Date the asset was purchased")


class AssetCreate(AssetBase):
    pass 


class AssetResponse(AssetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="ID of the asset")
    created_at: datetime = Field(description="Date the asset was registered in database")