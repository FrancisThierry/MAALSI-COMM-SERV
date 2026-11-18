from zeep import Client
from zeep.exceptions import Fault
from core.config import settings

class PurchaseSoapClient:
    def __init__(self):
        try:
            # Zeep va chercher le WSDL sur http://127.0.0.1:8000/purchase?wsdl
            self.client = Client(settings.WSDL_URL)
            print("✅ Client SOAP Purchase initialisé avec succès !")
        except Exception as e:
            print(f"⚠️ Impossible d'initialiser le client SOAP : {e}")
            self.client = None

    def valider_achat(self, data: dict):
        if not self.client:
            raise RuntimeError("Le client SOAP n'est pas initialisé.")
        
        try:
            # Appel de la méthode SOAP observée dans Postman
            response = self.client.service.ValiderAchat(
                Nom=data["nom"],
                Prenom=data["prenom"],
                Adresse=data["adresse"],
                Montant=data["montant"],
                IdAchat=data["id_achat"],
                DateAchat=data["date_achat"]
            )
            return response
        except Fault as error:
            raise ValueError(f"Erreur SOAP Fault : {error.message}")
        except Exception as e:
            raise RuntimeError(f"Erreur technique SOAP : {str(e)}")

purchase_soap_client = PurchaseSoapClient()