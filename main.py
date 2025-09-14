from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, APIRouter

from endpoint_configs.example import example_config
from tool_builder.tool_builder import ToolBuilder
from tool_handler.base import ToolHandler
from tool_handler.tool_call import ToolCall
from tool_handler.tool_response import ToolResponse


def _normalize_route_path(route: str) -> str:
    path = route if route.startswith("/") else "/" + route
    return path.replace(" ", "_").replace("{", "").replace("}", "")


def _bind_endpoint(router: APIRouter, handler: ToolHandler):
    cfg = handler.endpoint_config
    name = cfg.name
    path = _normalize_route_path(name)
    input_model = handler.endpoint_config.endpoint_input_schema
    output_model = handler.endpoint_config.endpoint_output_schema
    tool_call_type = ToolCall[input_model]
    response_type = ToolResponse[output_model]

    async def endpoint_fn(call: tool_call_type) -> response_type:
        result = await handler.handle_call(call)
        print(f"Endpoint '{name}' called with: {call}. Result: {result}")
        return result

    # Apply decorator programmatically to register the route
    router.post(path, name=name, summary=f"Dynamic endpoint for '{name}'", description=cfg.description)(endpoint_fn)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load endpoint configs and register routes using a router
    builder = ToolBuilder([example_config])
    router = APIRouter()
    for handler in builder.create_tool_handlers():
        _bind_endpoint(router, handler)

    app.include_router(router)

    yield


app = FastAPI(title="AutoTools API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # Disable reload when debugging to avoid child processes
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=False)
