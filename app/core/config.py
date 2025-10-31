from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "echomind-engine"
    version: str = "0.2.0"
    otlp_endpoint: str | None = None

settings = Settings()