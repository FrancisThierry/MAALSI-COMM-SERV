import datetime
import decimal
import os
import uuid
from wsgiref.simple_server import make_server

from pysimplesoap.server import SoapDispatcher, SoapFault, WSGISOAPHandler


MAX_REQUEST_SIZE = 1024 * 1024
NAMESPACE = "urn:maal-si:purchase"


def valider_achat(
    Nom=None,
    Prenom=None,
    Adresse=None,
    Montant=None,
    IdAchat=None,
    DateAchat=None,
):
    for name, value in (
        ("Nom", Nom),
        ("Prenom", Prenom),
        ("Adresse", Adresse),
        ("Montant", Montant),
        ("IdAchat", IdAchat),
        ("DateAchat", DateAchat),
    ):
        if value is None or (isinstance(value, str) and not value.strip()):
            raise SoapFault("ValidationError", f"{name} est obligatoire.")

    try:
        uuid.UUID(IdAchat)
    except (TypeError, ValueError) as error:
        raise SoapFault("ValidationError", "IdAchat doit être un UUID valide.") from error

    if not isinstance(DateAchat, datetime.datetime) or DateAchat.utcoffset() is None:
        raise SoapFault(
            "ValidationError",
            "DateAchat doit être une date ISO 8601 avec fuseau horaire.",
        )

    if not isinstance(Montant, decimal.Decimal) or not Montant.is_finite():
        raise SoapFault("ValidationError", "Montant doit être un nombre décimal fini.")

    return "Achat OK" if Montant > 0 else "Achat KO"


def create_service(host="127.0.0.1", port=8000):
    endpoint = f"http://{host}:{port}/purchase"
    dispatcher = SoapDispatcher(
        name="PurchaseService",
        location=endpoint,
        action=endpoint,
        namespace=NAMESPACE,
        prefix="tns",
    )
    dispatcher.register_function(
        "ValiderAchat",
        valider_achat,
        returns={"Retour": str},
        args={
            "Nom": str,
            "Prenom": str,
            "Adresse": str,
            "Montant": decimal.Decimal,
            "IdAchat": str,
            "DateAchat": datetime.datetime,
        },
    )
    return PurchaseSoapHandler(dispatcher)


class PurchaseSoapHandler(WSGISOAPHandler):
    def do_get(self, environ, start_response):
        if (
            environ.get("PATH_INFO") == "/purchase"
            and environ.get("QUERY_STRING", "").lower() == "wsdl"
        ):
            response = self.dispatcher.wsdl()
            start_response(
                "200 OK",
                [
                    ("Content-Type", "text/xml; charset=utf-8"),
                    ("Content-Length", str(len(response))),
                ],
            )
            return [response]

        return super().do_get(environ, start_response)

    def do_post(self, environ, start_response):
        if environ.get("PATH_INFO") != "/purchase":
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Service SOAP introuvable."]

        content_length = environ.get("CONTENT_LENGTH", "")
        if not content_length.isdecimal():
            start_response("400 Bad Request", [("Content-Type", "text/plain")])
            return [b"Content-Length invalide."]

        length = int(content_length)
        if length > MAX_REQUEST_SIZE:
            start_response("413 Payload Too Large", [("Content-Type", "text/plain")])
            return [b"Message SOAP trop volumineux."]

        request = environ["wsgi.input"].read(length).decode("utf-8")
        fault = {}
        response = self.dispatcher.dispatch(request, fault=fault)
        status = "500 Internal Server Error" if fault else "200 OK"
        start_response(
            status,
            [
                ("Content-Type", "text/xml; charset=utf-8"),
                ("Content-Length", str(len(response))),
            ],
        )
        return [response]


if __name__ == "__main__":
    host = os.getenv("PURCHASE_SERVICE_HOST", "127.0.0.1")
    port = int(os.getenv("PURCHASE_SERVICE_PORT", "8000"))
    application = create_service(host, port)
    print(f"Service SOAP prêt : http://{host}:{port}/purchase?wsdl")
    with make_server(host, port, application) as server:
        server.serve_forever()
