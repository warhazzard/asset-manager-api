from sqlalchemy.orm import Session
from app.models.asset import Asset 
from app.schemas.asset import AssetCreate
from typing import Optional


# Create a new asset
def create_asset(db: Session, asset: AssetCreate) -> Asset:
    db_asset = Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    
    return db_asset

def get_asset_by_id(db:Session, asset_id: int) -> Asset | None:
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_all_assets(db: Session, limit: int = 10, offset: int = 0, search: Optional[str] = None) -> list[Asset]:
    query = db.query(Asset)
    if search:
        query = query.filter(Asset.name.contains(search))
    return query.offset(offset).limit(limit).all()