"""Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field
from typing import Literal


class ProductRequest(BaseModel):
    """Incoming product analysis request."""
    id: int
    name: str
    price: float = Field(gt=0)
    rating: float = Field(ge=0, le=5)
    category: str


class BundleItem(BaseModel):
    """A single bundle recommendation."""
    name: str
    label: Literal["GOOD", "OVERHYPED", "AVOID"]
    reason: str


class AnalysisResponse(BaseModel):
    """Full analysis response returned to the frontend."""
    decision: Literal["BUY", "WAIT", "SKIP"]
    confidence: int = Field(ge=0, le=100)
    regret_risk: Literal["LOW", "MEDIUM", "HIGH"]
    factors: list[str]
    bundle: list[BundleItem]
    ai_explanation: str
