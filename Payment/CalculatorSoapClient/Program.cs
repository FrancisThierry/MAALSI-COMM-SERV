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