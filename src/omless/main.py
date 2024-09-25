# Python Included
import logging
from typing import AsyncGenerator

# FastAPI
from fastapi import FastAPI

# Middlewares
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .middlewares.exceptions import ExceptionMiddleware, exception_handlers
from .middlewares.metrics import MetricsMiddleware

# Imports
from .api import api_router
from .config import app_configs

from .logging import configure_logging
from .middlewares.rate_limiter import limiter

from contextlib import asynccontextmanager
from typing import AsyncGenerator

log = logging.getLogger(__name__)
configure_logging()

# we create the ASGI for the app
app = FastAPI(exception_handlers=exception_handlers, openapi_url="")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
#app.add_middleware(GZipMiddleware, minimum_size=1000)

@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Code executed on the Startup
    yield
    # Code executed on the Shutdown


# we create the Web API framework
api = FastAPI(
    **app_configs,
    lifespan=lifespan
)

api.add_middleware(MetricsMiddleware)

api.add_middleware(ExceptionMiddleware)


# we add all API routes to the Web API framework
api.include_router(api_router)

app.mount("/", app=api)