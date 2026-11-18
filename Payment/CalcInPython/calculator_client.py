from zeep import Client

# URL du WSDL du service Calculator
wsdl_url = 'http://www.dneonline.com/calculator.asmx?WSDL'

try:
    # Instanciation du client SOAP
    client = Client(wsdl=wsdl_url)

    a = 15
    b = 5

    # Appels des méthodes SOAP du service
    # Zeep permet de passer les arguments par nom ou par position
    somme = client.service.Add(intA=a, intB=b)
    soustraction = client.service.Subtract(intA=a, intB=b)
    multiplication = client.service.Multiply(intA=a, intB=b)
    division = client.service.Divide(intA=a, intB=b)

    # Affichage des résultats
    print(f"Addition ({a} + {b}) = {somme}")
    print(f"Soustraction ({a} - {b}) = {soustraction}")
    print(f"Multiplication ({a} * {b}) = {multiplication}")
    print(f"Division ({a} / {b}) = {division}")

except Exception as ex:
    print(f"Erreur lors de l'appel SOAP : {ex}")