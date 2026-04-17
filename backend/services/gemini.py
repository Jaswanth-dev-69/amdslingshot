"""Gemini API integration for generating natural language explanations."""

import os
import logging

from google import genai

from models.schemas import ProductRequest, BundleItem

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.0-flash"


def _build_prompt(
    product: ProductRequest,
    decision: str,
    confidence: int,
    regret_risk: str,
    factors: list[str],
    bundle: list[BundleItem],
) -> str:
    """Build a structured prompt for Gemini."""
    bundle_lines = "\n".join(
        f"  - {b.name} ({b.label}): {b.reason}" for b in bundle
    )
    factors_lines = "\n".join(f"  - {f}" for f in factors)

    return f"""You are an AI shopping assistant.
Explain in 2-3 sentences why this product should be BUY/WAIT/SKIP.
Use the provided factors and bundle insights. Be practical, not promotional.

Product Name: {product.name}
Price: ${product.price}
Rating: {product.rating}/5
Decision: {decision}
Confidence: {confidence}%
Regret Risk: {regret_risk}

Computed Factors:
{factors_lines}

Bundle Insights:
{bundle_lines}

Write your explanation now:"""


async def generate_explanation(
    product: ProductRequest,
    decision: str,
    confidence: int,
    regret_risk: str,
    factors: list[str],
    bundle: list[BundleItem],
) -> str:
    """
    Call Gemini API to generate a natural language explanation.
    Falls back to a rule-based explanation if the API call fails.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not set — using fallback explanation")
        return _fallback_explanation(product, decision, confidence, regret_risk)

    try:
        client = genai.Client(api_key=api_key)
        prompt = _build_prompt(product, decision, confidence, regret_risk, factors, bundle)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        text = response.text.strip()
        if text:
            return text
        return _fallback_explanation(product, decision, confidence, regret_risk)

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return _fallback_explanation(product, decision, confidence, regret_risk)


def _fallback_explanation(
    product: ProductRequest,
    decision: str,
    confidence: int,
    regret_risk: str,
) -> str:
    """Generate a deterministic fallback when Gemini is unavailable."""
    if decision == "BUY":
        return (
            f"{product.name} scores well across value, rating, and usability metrics. "
            f"With {confidence}% confidence and {regret_risk.lower()} regret risk, "
            f"this looks like a solid purchase at ${product.price}."
        )
    elif decision == "WAIT":
        return (
            f"{product.name} shows mixed signals — some factors are strong but others raise concerns. "
            f"At ${product.price} with {regret_risk.lower()} regret risk, "
            f"consider waiting for a better deal or more reviews."
        )
    else:
        return (
            f"{product.name} doesn't meet the threshold for a confident recommendation. "
            f"With {regret_risk.lower()} regret risk and only {confidence}% confidence, "
            f"you're better off exploring alternatives."
        )
