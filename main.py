import time
from src.utilities.company_util import company_details
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.core.logger import log_async, logger
from src.core.load_config import config
from src.core.db import log_global_error, close_db_pool, init_db_pool, log_error
from src.utilities.app_utils import generate_routes_json
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi import status
from src.routers import router as api_endpoints
from src.utilities.mjml_utils import compile_email_formats_mjml


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await log_async(logger.info, "Starting")
        await init_db_pool()
        await generate_routes_json()
        await compile_email_formats_mjml()
        yield  # Let FastAPI run
    except Exception as e:
        await log_error(e=e)
    finally:
        await log_async(logger.info, "Shutting down")
        await close_db_pool()


app = FastAPI(title=company_details['name']+" API",
              docs_url='/docs' if config['IsDevelopment'] else None,
              redoc_url='/redoc' if config['IsDevelopment'] else None,
              default_response_class=ORJSONResponse,
              lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def catch_exceptions_middleware(request: FastAPIRequest, call_next):
    body = await request.body()

    async def receive():
        return {"type": "http.request", "body": body}

    try:
        start_time = time.perf_counter()
        request._receive = receive
        response = await call_next(request)
        elapsed_time = time.perf_counter() - start_time

        # Log only if the request took more than 1 second
        if elapsed_time > 1:
            log_message = f"Slow Route Detected: {request.method} {request.url.path} - {elapsed_time:.4f}s"
            await log_async(logger.warning, log_message)
        return response
    except Exception as exc:
        request._receive = receive
        error_message = await log_global_error(exc, request, request_body=body.decode('utf-8'))
        return ORJSONResponse(
            status_code=500,
            content={"message": error_message},
        )

@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(request: FastAPIRequest, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)
        reformatted_message[field_string].append(msg)

    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid request", "errors": reformatted_message}
    )


app.include_router(api_endpoints)

if config['IsDevelopment']:
    app.mount("/static", StaticFiles(directory="static"), name="static")
