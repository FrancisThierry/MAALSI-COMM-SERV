from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from clients.soap_client import purchase_soap_client

router = APIRouter(prefix="/api/purchases", tags=["Purchases"])

# Modèle JSON attendu par le BFF depuis votre frontend (React, Vue, etc.)
class PurchaseInput(BaseModel):
    nom: str
    prenom: str
    adresse: str
    montant: float
    id_achat: str
    date_achat: datetime

@router.post("/", status_code=201)
def post_valider_achat(payload: PurchaseInput):
    try:
        # Conversion du payload Pydantic en dictionnaire pour Zeep
        # (Zeep gère la conversion automatique en XML SOAP enveloppé)
        result = purchase_soap_client.valider_achat(payload.dict())
        
        return {
            "status": "success",
            "soap_retour": result # Retourne le contenu de <tns:Retour>
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))