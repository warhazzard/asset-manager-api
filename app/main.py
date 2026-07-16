from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference


app = FastAPI(title="Asset Manager API")

@app.get("/")
def read_root():
    return {"status": "Asset Manager API is running"}

@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )