"""FastAPI application — Banking AI-Agent API Gateway."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.core.settings import get_settings
from app.core.schemas import (
    AgentRequest,
    AgentResponse,
    HealthResponse,
    ConfigResponse,
)
from app.clients.grpc_intent_client import IntentGRPCClient
from app.clients.ollama_client import OllamaClient
from app.agent.orchestrator import Orchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("api_gateway")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    settings = get_settings()

    # Startup: initialize clients
    logger.info("Starting API Gateway...")

    intent_client = IntentGRPCClient(
        host=settings.INTENT_SERVICE_HOST,
        port=settings.INTENT_SERVICE_PORT,
    )
    await intent_client.connect()

    ollama_client = OllamaClient(
        base_url=settings.OLLAMA_BASE_URL,
        model_name=settings.OLLAMA_MODEL_NAME,
        timeout=settings.OLLAMA_TIMEOUT,
    )

    # Store clients in app state
    app.state.intent_client = intent_client
    app.state.ollama_client = ollama_client
    app.state.settings = settings

    logger.info("API Gateway started successfully")
    logger.info("Intent Service: %s:%d", settings.INTENT_SERVICE_HOST, settings.INTENT_SERVICE_PORT)
    logger.info("Ollama: %s (model: %s)", settings.OLLAMA_BASE_URL, settings.OLLAMA_MODEL_NAME)

    yield

    # Shutdown: cleanup clients
    logger.info("Shutting down API Gateway...")
    await intent_client.close()
    await ollama_client.close()
    logger.info("API Gateway shut down")


app = FastAPI(
    title="Banking AI-Agent Gateway",
    description="API Gateway for the Banking AI Agentic System",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check whether the system is running."""
    return HealthResponse(status="healthy")


@app.get("/config", response_model=ConfigResponse)
async def get_config():
    """Return the current system configuration."""
    settings = app.state.settings
    return ConfigResponse(
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        ollama_model=settings.OLLAMA_MODEL_NAME,
        intent_service_host=settings.INTENT_SERVICE_HOST,
        intent_service_port=settings.INTENT_SERVICE_PORT,
    )


@app.post("/run-agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Execute the full agentic workflow.

    Receives a customer message, calls Intent Service through gRPC,
    executes workflow nodes, calls Ollama for response generation,
    and returns the final structured result.
    """
    try:
        orchestrator = Orchestrator(
            intent_client=app.state.intent_client,
            ollama_client=app.state.ollama_client,
        )
        result = await orchestrator.run(request.message)
        return AgentResponse(**result)

    except Exception as e:
        logger.error("Agent workflow failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Agent workflow failed: {str(e)}",
        )
