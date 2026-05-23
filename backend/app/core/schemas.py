"""Pydantic schemas for API Gateway request/response models."""

from typing import Optional
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Request body for POST /run-agent."""

    message: str = Field(
        ..., min_length=1, max_length=2000, description="Customer message"
    )


class IntentResult(BaseModel):
    """Intent classification result."""

    intent: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str = ""


class PolicyInfo(BaseModel):
    """Banking policy information."""

    policy_id: str
    title: str
    content: str
    applicable: bool = True


class AgentResponse(BaseModel):
    """Full response from the agent workflow."""

    intent: IntentResult
    priority: str = Field(..., description="low | medium | high | critical")
    policy: Optional[PolicyInfo] = None
    validation_passed: bool
    routed_to: str
    draft_response: str
    missing_info: Optional[str] = None
    next_action: str = ""


class HealthResponse(BaseModel):
    """Response for GET /health."""

    status: str = "healthy"


class ConfigResponse(BaseModel):
    """Response for GET /config."""

    app_name: str
    version: str
    ollama_model: str
    intent_service_host: str
    intent_service_port: int
