from concurrent import futures
import grpc
import product_pb2
import product_pb2_grpc

class ProductServiceServicer(product_pb2_grpc.ProductServiceServicer):
    def GetProductByCategory(self, request, context):
        print(f"📥 [gRPC Server] Requête reçue pour la catégorie : '{request.category}'")
        
        # Base de données simulée pour la démo
        mock_db = {
            "electronique": [
                product_pb2.ProductItem(id=1, name="Casque Bluetooth", price=99.99, category="electronique"),
                product_pb2.ProductItem(id=2, name="Clavier Mécanique", price=79.50, category="electronique"),
            ],
            "maison": [
                product_pb2.ProductItem(id=3, name="Lampe LED Design", price=45.00, category="maison"),
                product_pb2.ProductItem(id=4, name="Cafetière Filtre", price=59.90, category="maison"),
            ]
        }
        
        # Récupération des produits ou liste vide si la catégorie n'existe pas
        items = mock_db.get(request.category.lower(), [])
        
        print(f"📤 [gRPC Server] {len(items)} produits trouvés, envoi de la réponse.")
        return product_pb2.ProductResponseList(products=items)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🚀 Serveur gRPC démarré et en écoute sur le port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()