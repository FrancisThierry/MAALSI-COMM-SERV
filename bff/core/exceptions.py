# Gestion centralisÃ©e des erreurs (SOAP, gRPC, REST)
from fastapi import HTTPException

def handle_soap_error(error):
    raise HTTPException(status_code=400, detail=f"SOAP Fault: {str(error)}")

def handle_grpc_error(error):
    raise HTTPException(status_code=502, detail=f"gRPC Error [{error.code().name}]: {error.details()}")