from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.database import engine 
from app.models import asset, user
from app.routers import asset as asset_router


# Create all tables in database
user.Base.metadata.create_all(bind=engine)
asset.Base.metadata.create_all(bind=engine)


#  Initialize FastAPI app
app = FastAPI(title="Asset Manager API")
app.include_router(asset_router.router)


@app.get("/", include_in_schema=False)
def read_root():
    return {"status": "Asset Manager API is running"}


# Scalar API documentation endpoint
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )


