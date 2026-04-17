"""Rule-based scoring engine for product analysis."""

from models.schemas import ProductRequest

# Average prices per category (heuristic baseline)
CATEGORY_AVG_PRICE: dict[str, float] = {
    "electronics": 200.0,
    "clothing": 60.0,
    "books": 20.0,
    "home": 80.0,
    "sports": 100.0,
    "beauty": 40.0,
    "toys": 35.0,
    "grocery": 15.0,
    "automotive": 150.0,
    "health": 50.0,
}

# Assumed usage frequency by category (1-10 scale)
CATEGORY_USAGE_FREQ: dict[str, int] = {
    "electronics": 8,
    "clothing": 7,
    "books": 5,
    "home": 7,
    "sports": 5,
    "beauty": 6,
    "toys": 4,
    "grocery": 10,
    "automotive": 6,
    "health": 7,
}

DEFAULT_AVG_PRICE = 75.0
DEFAULT_USAGE_FREQ = 5


def compute_score(product: ProductRequest) -> tuple[int, list[str], dict[str, int]]:
    """
    Compute a 0-100 score and gather decision factors.

    Scoring breakdown (100 total):
      - Rating quality:     0-30 points
      - Price-to-value:     0-30 points
      - Usage frequency:    0-25 points
      - Return risk bonus:  0-15 points
    """
    factors: list[str] = []

    def add_factor(text: str) -> None:
        if text not in factors:
            factors.append(text)

    cat = product.category.lower()

    # --- Rating quality (max 30) ---
    rating_score = int(round((product.rating / 5.0) * 30))
    if product.rating >= 4.0:
        add_factor(f"Rating of {product.rating}/5 indicates strong user satisfaction")
    elif product.rating < 3.5:
        add_factor(f"Rating of {product.rating}/5 indicates lower user satisfaction")

    # --- Price-to-value ratio (max 30) ---
    avg_price = CATEGORY_AVG_PRICE.get(cat, DEFAULT_AVG_PRICE)
    price_ratio = avg_price / max(product.price, 1.0)  # higher = better value
    price_score = int(round(min(price_ratio * 30, 30)))  # cap at 30
    if product.price < avg_price:
        add_factor(f"Price is {round((1 - product.price / avg_price) * 100)}% below category average")
    elif product.price > avg_price:
        add_factor(f"Price is {round((product.price / avg_price - 1) * 100)}% above category average")

    if product.rating >= 4.0 and product.price < avg_price:
        add_factor("Strong value for money based on rating and price")
    elif product.rating < 3.5 and product.price > avg_price:
        add_factor("Poor value for money considering price and rating")

    # --- Usage frequency (max 25) ---
    usage = CATEGORY_USAGE_FREQ.get(cat, DEFAULT_USAGE_FREQ)
    usage_score = int(round((usage / 10.0) * 25))
    if usage_score >= 17:
        add_factor("Product likely to be used frequently")
    elif usage_score <= 10:
        add_factor("Low expected usage reduces value")

    # --- Return risk heuristic (max 15) ---
    # Lower return risk = higher bonus
    return_risk = 0.0
    if product.rating < 3.5:
        return_risk += 0.4
    if price_ratio < 0.6:
        return_risk += 0.3
    if usage < 4:
        return_risk += 0.3
    risk_adjustment = int(round((1.0 - min(return_risk, 1.0)) * 15))
    if return_risk >= 0.5:
        add_factor("Higher probability of returns or dissatisfaction")

    if len(factors) < 3 and 3.5 <= product.rating < 4.0:
        add_factor("Rating trend is moderate and may limit confidence")
    if len(factors) < 3 and product.price == avg_price:
        add_factor("Price is in line with the category average")
    if len(factors) < 3 and 10 < usage_score < 17:
        add_factor("Expected usage is moderate for this category")
    if len(factors) < 3 and return_risk < 0.5:
        add_factor("Return risk remains controlled under current inputs")

    factors = factors[:5]

    score_breakdown = {
        "rating_score": rating_score,
        "price_score": price_score,
        "usage_score": usage_score,
        "risk_adjustment": risk_adjustment,
    }

    final_score = int(min(max(sum(score_breakdown.values()), 0), 100))
    return final_score, factors, score_breakdown


def score_to_decision(score: int) -> str:
    """Map a numeric score to a decision label."""
    if score > 70:
        return "BUY"
    elif score >= 40:
        return "WAIT"
    else:
        return "SKIP"
