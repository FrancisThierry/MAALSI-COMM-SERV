import io
import unittest
from xml.etree import ElementTree

from purchase_service import create_service


SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"
SERVICE_NS = "urn:maal-si:purchase"
service = create_service()


def call_service(method, body=b"", query_string="", path="/"):
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query_string,
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "8000",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "http",
        "wsgi.input": io.BytesIO(body),
        "wsgi.errors": io.StringIO(),
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
        "CONTENT_LENGTH": str(len(body)),
    }
    response = {}

    def start_response(status, headers):
        response["status"] = status
        response["headers"] = dict(headers)

    response["body"] = b"".join(service(environ, start_response))
    return response


class PurchaseServiceTests(unittest.TestCase):
    def test_wsdl_declares_all_required_purchase_fields(self):
        response = call_service("GET", query_string="wsdl", path="/purchase")

        self.assertTrue(response["status"].startswith("200"))
        wsdl = ElementTree.fromstring(response["body"])
        for field in ("Nom", "Prenom", "Adresse", "Montant", "IdAchat", "DateAchat"):
            self.assertIsNotNone(
                wsdl.find(f".//{{http://www.w3.org/2001/XMLSchema}}element[@name='{field}']")
            )
        self.assertNotIn(b'minOccurs="0"', response["body"])
        self.assertIn(b"ValiderAchatResponse", response["body"])
        self.assertIn(b'name="Retour"', response["body"])

    def test_soap_request_accepts_and_rejects_by_amount(self):
        for amount, expected in (("12.50", "Achat OK"), ("0", "Achat KO"), ("-1", "Achat KO")):
            with self.subTest(amount=amount):
                response = call_service("POST", soap_request(amount), path="/purchase")

                self.assertTrue(response["status"].startswith("200"))
                envelope = ElementTree.fromstring(response["body"])
                result = envelope.find(
                    f".//{{{SERVICE_NS}}}ValiderAchatResponse/{{{SERVICE_NS}}}Retour"
                )
                self.assertEqual(result.text, expected)

    def test_missing_field_returns_soap_fault(self):
        body = soap_request("5").replace(b"<tns:Prenom>Lea</tns:Prenom>", b"")
        response = call_service("POST", body, path="/purchase")

        self.assertTrue(response["status"].startswith("500"))
        envelope = ElementTree.fromstring(response["body"])
        fault = envelope.find(f".//{{{SOAP_NS}}}Fault")
        self.assertIsNotNone(fault)
        self.assertIn("Prenom est obligatoire", fault.findtext("faultstring"))

    def test_invalid_uuid_and_timezone_return_soap_faults(self):
        requests = (
            soap_request("5").replace(
                b"c6a9c35d-6947-4581-8c82-a5d045ad9345",
                b"not-a-uuid",
            ),
            soap_request("5").replace(
                b"2026-11-18T10:00:00Z",
                b"2026-11-18T10:00:00",
            ),
        )
        for body in requests:
            with self.subTest(body=body):
                response = call_service("POST", body, path="/purchase")

                self.assertTrue(response["status"].startswith("500"))
                envelope = ElementTree.fromstring(response["body"])
                self.assertIsNotNone(envelope.find(f".//{{{SOAP_NS}}}Fault"))


def soap_request(amount):
    return f"""<?xml version="1.0"?>
    <soap:Envelope xmlns:soap="{SOAP_NS}" xmlns:tns="{SERVICE_NS}">
      <soap:Body>
        <tns:ValiderAchat>
          <tns:Nom>Martin</tns:Nom>
          <tns:Prenom>Lea</tns:Prenom>
          <tns:Adresse>10 rue des Lilas</tns:Adresse>
          <tns:Montant>{amount}</tns:Montant>
          <tns:IdAchat>c6a9c35d-6947-4581-8c82-a5d045ad9345</tns:IdAchat>
          <tns:DateAchat>2026-11-18T10:00:00Z</tns:DateAchat>
        </tns:ValiderAchat>
      </soap:Body>
    </soap:Envelope>""".encode()


if __name__ == "__main__":
    unittest.main()
