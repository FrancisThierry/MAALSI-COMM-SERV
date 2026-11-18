import grpc
import product_pb2
import product_pb2_grpc

with grpc.insecure_channel('localhost:50051') as channel:
    stub = product_pb2_grpc.ProductServiceStub(channel)
    response = stub.GetProductByCategory(product_pb2.ProductRequest(category="electronique"))
    for p in response.products:
        print(f"Produit trouvé : {p.name} - {p.price}€")