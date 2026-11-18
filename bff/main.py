from fastapi import FastAPI
from core.config import settings
from routers import users, orders, purchase

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="BFF agnostique (SOAP, gRPC, REST)",
    version="1.0.0"
)

# Inclusion des routeurs
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(purchase.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "BFF is running"}