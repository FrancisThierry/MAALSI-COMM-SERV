import grpc
from core.config import settings

# Canal gRPC global (Ã  adapter avec vos stubs gÃ©nÃ©rÃ©s)
# channel = grpc.insecure_channel(settings.GRPC_BACKEND_URL)