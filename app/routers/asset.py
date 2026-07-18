from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db 
from app.crud import asset as crud_asset
from app.schemas.asset import AssetCreate, AssetResponse 
from app.models.asset import Asset

# Create a new router instance for asset-related endpoints
router = APIRouter(
    prefix="/assets",
    tags=["assets"],
)


# Define an endpoint for creating a new asset
@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_new_asset(asset:AssetCreate, db: Session = Depends(get_db)) -> Asset:
    return crud_asset.create_asset(db, asset) 


# Define an endpoint for retrieving all assets
@router.get("/", response_model=list[AssetResponse])
def get_all_assets(db: Session = Depends(get_db)) -> list[Asset]:
    return crud_asset.get_all_assets(db)


# Define an endpoint for retrieving an asset by its ID
@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset_by_id(asset_id: int, db: Session = Depends(get_db)) -> Asset | None:
    asset = crud_asset.get_asset_by_id(db, asset_id)

    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    return asset 