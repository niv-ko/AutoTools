from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

from endpoint_configs.load import load_endpoint_configs
from tool_handler.tool_handler import ToolHandler
from extraction_configs.schema import ExtractionConfig


def _normalize_route_path(route) -> str:
    try:
        path = route.as_posix()
    except AttributeError:
        path = str(route)
    if not path.startswith("/"):
        path = "/" + path
    return path


def _bind_endpoint(router: APIRouter, handler: ToolHandler, path: str, name: str, description: str):
    Model = handler.create_tool_call()

    async def endpoint_fn(body: Model):  # type: ignore
        result = handler.handle_call(body)
        return JSONResponse(content=result)

    # Apply decorator programmatically to register the route
    router.post(path, name=name, summary=f"Dynamic endpoint for '{name}'", description=description)(endpoint_fn)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load endpoint configs and register routes using a router
    router = APIRouter()
    for cfg in load_endpoint_configs():
        handler = ToolHandler(
            endpoint_config=cfg,
            extraction_config=ExtractionConfig(parameter_extraction_methods=[], parameters_requirements=[]),
        )
        path = _normalize_route_path(cfg.route)
        _bind_endpoint(router, handler, path, cfg.name, cfg.description)

    app.include_router(router)

    yield


app = FastAPI(title="AutoTools API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}
