from sqlalchemy.orm import Session
from app.models.asset import Asset 
from app.schemas.asset import AssetCreate


# Create a new asset
def create_asset(db: Session, asset: AssetCreate) -> Asset:
    db_asset = Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    
    return db_asset

def get_asset_by_id(db:Session, asset_id: int) -> Asset | None:
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_all_assets(db: Session) -> list[Asset]:
    return db.query(Asset).all()