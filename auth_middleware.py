from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from jwt_utils import decode_jwt_token
import logging

logger = logging.getLogger("zenark.middleware")

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Intercepts requests to check for JWT in Authorization header.
        Attaches user payload to request.state.user if valid.
        """
        # 1. Bypass auth for internal/public static routes if needed
        # (Though soft middleware doesn't strictly need this, it's good for performance)
        exempt_paths = ["/docs", "/openapi.json", "/redoc"]
        if any(request.url.path.startswith(path) for path in exempt_paths):
            return await call_next(request)

        # 2. Extract Authorization header
        auth_header = request.headers.get("Authorization")
        
        # Initialize state.user to None
        request.state.user = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # 3. Decode and validate
                payload = decode_jwt_token(token)
                
                # 4. Success! Attach to state
                request.state.user = payload
                # logger.info(f"✅ Authenticated: {payload.get('email')}")
            except Exception as e:
                # We don't raise 401 here to stay "Soft" - individual routes can check state.user
                logger.warning(f"⚠️  JWT Validation failed: {e}")
        
        # 5. Continue to the next handler
        response = await call_next(request)
        return response
