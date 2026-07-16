from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.database import engine 
from app.models import user, asset


#  Initialize FastAPI app
app = FastAPI(title="Asset Manager API")

@app.get("/")
def read_root():
    return {"status": "Asset Manager API is running"}


# Scalar API documentation endpoint
@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )


# Create all tables in database
user.Base.metadata.create_all(bind=engine)
asset.Base.metadata.create_all(bind=engine)