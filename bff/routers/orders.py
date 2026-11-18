from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Orders"])

@router.get("/orders")
def list_orders():
    return [{"order_id": 1, "item": "Produit A"}]