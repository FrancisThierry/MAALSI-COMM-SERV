import grpc
import product_pb2
import product_pb2_grpc

class ProductGrpcClient:
    def __init__(self, host="localhost:50051"):
        # Établissement du canal gRPC vers le microservice
        self.channel = grpc.insecure_channel(host)
        self.stub = product_pb2_grpc.ProductServiceStub(self.channel)

    def get_products_by_category(self, category: str):
        try:
            request = product_pb2.ProductRequest(category=category)
            response = self.stub.GetProductByCategory(request)
            
            # Transformation des objets gRPC en dictionnaires Python purs (pour FastAPI/JSON)
            return [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "category": p.category
                }
                for p in response.products
            ]
        except grpc.RpcError as e:
            print(f"⚠️ Erreur gRPC : {e.details()}")
            return []

# Instance unique réutilisable dans le BFF
grpc_client = ProductGrpcClient()