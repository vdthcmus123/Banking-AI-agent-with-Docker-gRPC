"""Pydantic schemas for Intent Service."""

from pydantic import BaseModel, Field


class IntentResult(BaseModel):
    """Result of intent classification."""

    intent: str = Field(..., description="Predicted banking intent")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    reason: str = Field("", description="Explanation for the classification")
