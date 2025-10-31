import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

HEADER_CID = "X-Correlation-Id"
HEADER_API_VERSION = "X-API-Version"

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_version: str):
        super().__init__(app)
        self.api_version = api_version

    async def dispatch(self, request: Request, call_next):
        cid = request.headers.get(HEADER_CID) or str(uuid.uuid4())
        request.state.correlation_id = cid
        response: Response = await call_next(request)
        response.headers[HEADER_CID] = cid
        response.headers[HEADER_API_VERSION] = self.api_version
        return response
