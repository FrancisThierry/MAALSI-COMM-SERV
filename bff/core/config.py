import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Frontend BFF"
    WSDL_URL: str = os.getenv("WSDL_URL", "http://127.0.0.1:8000/purchase?wsdl")
    GRPC_BACKEND_URL: str = os.getenv("GRPC_BACKEND_URL", "localhost:50051")
    REST_BACKEND_URL: str = os.getenv("REST_BACKEND_URL", "http://localhost:5000")

    class Config:
        env_file = ".env"

settings = Settings()

