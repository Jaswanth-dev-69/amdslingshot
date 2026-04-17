"""Regret risk assessment based on product characteristics."""

from models.schemas import ProductRequest
from logic.scoring import CATEGORY_USAGE_FREQ, DEFAULT_USAGE_FREQ


def assess_regret_risk(product: ProductRequest, score: int) -> str:
    """
    Determine regret risk level.

    Factors considered:
      - Low usage frequency → higher regret
      - Low rating → higher regret
      - Low overall score → higher regret
      - High price relative to score → higher regret

    Returns: "LOW", "MEDIUM", or "HIGH"
    """
    risk_points = 0
    cat = product.category.lower()
    usage = CATEGORY_USAGE_FREQ.get(cat, DEFAULT_USAGE_FREQ)

    # Low usage frequency
    if usage <= 3:
        risk_points += 3
    elif usage <= 5:
        risk_points += 1

    # Low rating
    if product.rating < 3.0:
        risk_points += 3
    elif product.rating < 3.5:
        risk_points += 2
    elif product.rating < 4.0:
        risk_points += 1

    # Low overall score
    if score < 40:
        risk_points += 3
    elif score < 55:
        risk_points += 2
    elif score < 70:
        risk_points += 1

    # Expensive + low score combo
    if product.price > 200 and score < 60:
        risk_points += 2

    # Map to risk level
    if risk_points >= 6:
        return "HIGH"
    elif risk_points >= 3:
        return "MEDIUM"
    else:
        return "LOW"
