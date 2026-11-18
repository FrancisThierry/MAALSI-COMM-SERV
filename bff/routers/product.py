from fastapi import APIRouter, Query
from clients.grpc_client import grpc_client

router = APIRouter(prefix="/api/products", tags=["Products (gRPC)"])

@router.get("/search")
def search_products(category: str = Query(..., description="Ex: electronique ou maison")):
    """
    Endpoint REST géré par le BFF, qui délégue la recherche au microservice gRPC en interne.
    """
    # Appel du client gRPC
    products = grpc_client.get_products_by_category(category)
    
    return {
        "protocol_gateway": "REST (FastAPI) ➔ gRPC ➔ Microservice",
        "category_searched": category,
        "count": len(products),
        "results": products
    }