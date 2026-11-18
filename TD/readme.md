## SOAP
### En dot net

Pour consommer le service SOAP `[http://www.dneonline.com/calculator.asmx?WSDL](http://www.dneonline.com/calculator.asmx?WSDL)` dans un projet .NET moderne (.NET 6, 8, etc.), la méthode recommandée consiste à générer automatiquement le client proxy à l'aide de l'outil **dotnet-svcutil**.

### 1. Création du projet et génération du client

Ouvrez un terminal et exécutez les commandes suivantes :

```bash
# 1. Créer une application console (ou utiliser votre projet existant)
dotnet new console -n CalculatorSoapClient
cd CalculatorSoapClient

# 2. Installer l'outil dotnet-svcutil (s'il n'est pas déjà installé)
dotnet tool install --global dotnet-svcutil

# 3. Générer le code client à partir du WSDL
dotnet-svcutil http://www.dneonline.com/calculator.asmx?WSDL

```

Cette dernière commande va automatiquement :

* Ajouter les packages NuGet nécessaires (`System.ServiceModel.*`) à votre fichier `.csproj`.
* Créer un fichier `ServiceReference/Reference.cs` contenant la classe `CalculatorSoapClient` ainsi que les méthodes `AddAsync`, `SubtractAsync`, `MultiplyAsync` et `DivideAsync`.

---

### 2. Implémentation en C#

Remplacez le contenu de votre fichier `Program.cs` par le code suivant :

```csharp
using System;
using System.Threading.Tasks;
using ServiceReference; // Namespace généré par défaut par dotnet-svcutil

class Program
{
    static async Task Main(string[] args)
    {
        // Instanciation du client avec la configuration SOAP 1.1 par défaut
        using var client = new CalculatorSoapClient(
            CalculatorSoapClient.EndpointConfiguration.CalculatorSoap
        );

        try
        {
            int a = 15;
            int b = 5;

            // Appels asynchrones aux méthodes du Web Service
            int somme = await client.AddAsync(a, b);
            int soustraction = await client.SubtractAsync(a, b);
            int multiplication = await client.MultiplyAsync(a, b);
            int division = await client.DivideAsync(a, b);

            Console.WriteLine($"Addition ({a} + {b}) = {somme}");
            Console.WriteLine($"Soustraction ({a} - {b}) = {soustraction}");
            Console.WriteLine($"Multiplication ({a} * {b}) = {multiplication}");
            Console.WriteLine($"Division ({a} / {b}) = {division}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Erreur lors de l'appel SOAP : {ex.Message}");
        }
    }
}

```

### 3. Exécution

Lancez l'application avec :

```bash
dotnet run

```

