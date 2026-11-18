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
## Le Gprc

# Module Pédagogique : Architecture gRPC et Protocol Buffers

L'évolution des architectures logicielles modernes, caractérisée par la transition vers des microservices distribués et des passerelles applicatives de type BFF (*Backend For Frontend*), exige des mécanismes de communication inter-services d'une grande rigueur et d'une performance accrue. C'est dans ce contexte que s'inscrit **gRPC**, fondé sur le principe des appels de procédures distantes et structuré autour du contrat immuable **Protocol Buffers**.

---

## I. Le Paradigme de la Communication Distante

### 1. Limites des approches textuelles traditionnelles

Durant de nombreuses années, le style architectural REST, couplé au format textuel JSON et au protocole HTTP/1.1, a dominé la conception des APIs. Si cette approche s'est révélée universelle, elle montre des limites structurelles dans le cadre de communications intensives entre microservices :

* **La verbosité du texte :** Les données textuelles nécessitent un encodage et un décodage textuel lourd.
* **L'absence de typage strict natif :** Le JSON repose sur des conventions de nommage et nécessite des validateurs externes (tels que Pydantic) pour s'assurer de l'intégrité des structures.
* **La surcharge de parsing :** L'analyse syntaxique de chaînes de caractères complexes pèse lourdement sur la consommation processeur lors d'appels à haute fréquence.

### 2. Le retour du modèle RPC (Remote Procedure Calls)

gRPC réhabilite le concept classique des RPC en privilégiant l'invocation synchrone de fonctions distantes. Cette architecture s'affranchit de la manipulation sémantique de ressources (liée aux verbes HTTP de REST) pour se concentrer sur l'exécution directe d'actions. Le client invoque une méthode sur un serveur distant de manière transparente, comme s'il s'agissait de code local, réduisant ainsi la complexité de la couche d'échange.

---

## II. La Souveraineté du Contrat : Le Fichier `.proto`

Le fondement de tout échange gRPC réside dans un contrat formel consigné au sein d'un fichier portant l'extension **`.proto`**. Ce fichier constitue la source unique de vérité (*Single Source of Truth*) pour l'ensemble des services communicants.

1. **L'agnosticisme technologique :** Le contrat est totalement indépendant des langages de programmation utilisés. Qu'un microservice soit développé en Python, C#, Go ou Java, tous s'alignent sur la même définition syntaxique.
2. **Le typage strict et la sérialisation binaire :** À la différence des formats textuels, Protocol Buffers (Protobuf) compile les structures de données en un **flux binaire compact**. Chaque champ est identifié par un tag numérique unique. Lors de la transmission, seuls cet identifiant et sa valeur transitent, éliminant la répétition des clés textuelles et réduisant drastiquement la volumétrie réseau.
3. **La génération automatique des stubs :** Par la compilation du fichier de définition, les interfaces client et serveur sont générées automatiquement, garantissant une stricte conformité syntaxique et sémantique sans nécessiter de codage manuel de la sérialisation.

---

## III. L'Optimisation du Transport par HTTP/2

La haute performance de gRPC découle directement de l'utilisation native du protocole de transport **HTTP/2**, marquant une rupture nette avec HTTP/1.1.

* **Le multiplexage :** Plusieurs requêtes et réponses transitent simultanément sur une unique connexion TCP persistante, éliminant la congestion séquentielle et le blocage de tête de ligne (*Head-of-Line Blocking*).
* **Le streaming natif :** Les flux unilatéraux (Server Streaming, Client Streaming) ou bidirectionnels sont pris en charge de manière native, permettant des communications continues, asynchrones et en temps réel.
* **La compression des en-têtes (HPACK) :** Les métadonnées réseau sont compressées dynamiquement, réduisant le trafic superflu et maximisant la bande passante utile.

---

## IV. La Génération Polyglotte des Interfaces (Stubs)

La puissance opérationnelle de gRPC réside dans sa capacité à produire, à partir d'un unique fichier `.proto`, le code source d'implémentation pour des écosystèmes hétérogènes.

### 1. Écosystème Python

La génération s'appuie sur le paquet officiel `grpcio-tools`, intégrant le compilateur `protoc` :

```powershell
python -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/product.proto

```

* `--python_out` génère le code de sérialisation des messages (`_pb2.py`).
* `--grpc_python_out` génère les classes de services et de stubs (`_pb2_grpc.py`).

### 2. Écosystème .NET (C#)

La génération est intégrée de manière native au cycle de compilation via le système MSBuild et les packages NuGet (`Google.Protobuf`, `Grpc.Tools`). La déclaration s'effectue directement dans le fichier projet (`.csproj`) :

```xml
<ItemGroup>
  <Protobuf Include="Protos\product.proto" GrpcServices="Both" />
</ItemGroup>

```

À la compilation (`dotnet build`), les classes C# fortement typées sont actualisées en arrière-plan.

### 3. Écosystème PHP

L'intégration requiert l'outil binaire universel `protoc` couplé aux plugins spécifiques gRPC :

```bash
protoc -I=protos \
  --php_out=./generated \
  --grpc_out=./generated \
  --plugin=protoc-gen-grpc=/chemin/vers/grpc_php_plugin \
  protos/product.proto

```

Cela produit les classes de définition des messages en PHP pur ainsi que les clients gérant l'émission des requêtes.

---
