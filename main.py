from contextlib import asynccontextmanager
from typing import Type

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

from endpoint_configs.example import example_config
from endpoint_configs.schema import EndpointSchema
from extraction_handler.lang_graph.lang_graph import GraphExtractionHandler
from request_generator.impl.dummy import DummyRequestGenerator
from tool_handler.base import ToolHandler
from extraction_configs.schema import ExtractionConfig, ParameterExtractionMethod, ExtractionMethod
from tool_handler.tool_call import ToolCall
from tool_handler.tool_response import ToolResponse


def _normalize_route_path(route) -> str:
    try:
        path = route.as_posix()
    except AttributeError:
        path = str(route)
    if not path.startswith("/"):
        path = "/" + path
    return path


def _bind_endpoint(router: APIRouter, handler: ToolHandler, path: str, name: str, description: str):
    input_model = handler.endpoint_config.endpoint_input_schema
    output_model = handler.endpoint_config.endpoint_output_schema
    tool_call_type = ToolCall[input_model]
    response_type = ToolResponse[output_model]

    async def endpoint_fn(call: tool_call_type) -> response_type :
        result = await handler.handle_call(call)
        print(f"Endpoint '{name}' called with: {call}. Result: {result}")
        return result

    # Apply decorator programmatically to register the route
    router.post(path, name=name, summary=f"Dynamic endpoint for '{name}'", description=description)(endpoint_fn)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load endpoint configs and register routes using a router
    router = APIRouter()
    for cfg in [example_config]:
        handler = ToolHandler(
            endpoint_config=cfg,
            extraction_config=ExtractionConfig(
                parameter_extraction_methods=[
                    ParameterExtractionMethod(
                        parameter_name='a',
                        extraction_method=ExtractionMethod(
                            extractor_name="dummy"
                        )
                    ),
                    ParameterExtractionMethod(
                        parameter_name='b',
                        extraction_method=ExtractionMethod(
                            extractor_name="dummy"
                        )
                    )
                ]
            ),
            extraction_handler_cls=GraphExtractionHandler,
            request_generator_cls=DummyRequestGenerator
        )
        path = _normalize_route_path(cfg.name)
        _bind_endpoint(router, handler, path, cfg.name, cfg.description)

    app.include_router(router)

    yield


app = FastAPI(title="AutoTools API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    # Disable reload when debugging to avoid child processes
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=False)
