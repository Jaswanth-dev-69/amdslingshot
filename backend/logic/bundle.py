"""Bundle generation with classification for each product category."""

from models.schemas import BundleItem

# Pre-defined bundles per category.
# Each item: (name, label, reason)
CATEGORY_BUNDLES: dict[str, list[tuple[str, str, str]]] = {
    "electronics": [
        ("Premium Carry Case", "GOOD", "High long-term usage and strong user satisfaction"),
        ("Extended Warranty (1yr)", "OVERHYPED", "Often purchased but rarely claimed — low ROI"),
        ("Third-party Charger", "AVOID", "Known compatibility and safety issues"),
        ("Screen Protector", "GOOD", "Low cost, high damage prevention value"),
        ("Bluetooth Adapter", "OVERHYPED", "Most modern devices already include Bluetooth"),
    ],
    "clothing": [
        ("Fabric Care Kit", "GOOD", "Extends garment lifespan significantly"),
        ("Matching Accessories Set", "OVERHYPED", "Trendy but rarely reused across outfits"),
        ("Express Alterations", "GOOD", "Ensures perfect fit and reduces return likelihood"),
        ("Clothing Insurance", "AVOID", "Cost rarely justified for everyday wear"),
    ],
    "books": [
        ("Reading Light", "GOOD", "Enhances reading experience, especially for print"),
        ("Book Subscription Add-on", "OVERHYPED", "Often leads to unread backlog"),
        ("Premium Bookmark Set", "GOOD", "Low cost, practical daily use"),
        ("Audiobook Bundle", "OVERHYPED", "Useful only if listener prefers audio format"),
    ],
    "home": [
        ("Installation Service", "GOOD", "Saves time and ensures proper setup"),
        ("Extended Warranty (2yr)", "OVERHYPED", "Most home items outlast warranty periods"),
        ("Off-brand Replacement Parts", "AVOID", "Compatibility and durability concerns"),
        ("Cleaning Kit", "GOOD", "Essential for maintenance and longevity"),
    ],
    "sports": [
        ("Carrying Bag", "GOOD", "Practical for transport and storage"),
        ("Performance Supplements", "OVERHYPED", "Benefits vary widely, often unnecessary"),
        ("Premium Grip Tape", "GOOD", "Low cost with noticeable performance improvement"),
        ("Knockoff Accessories", "AVOID", "Poor durability and potential safety risks"),
    ],
    "beauty": [
        ("Application Brush Set", "GOOD", "Improves product application and results"),
        ("Deluxe Sample Bundle", "OVERHYPED", "Tiny sizes rarely provide meaningful trial"),
        ("Organic Cotton Pads", "GOOD", "Eco-friendly and gentle on skin"),
        ("Counterfeit Alternatives", "AVOID", "Risk of skin irritation and harmful ingredients"),
    ],
    "toys": [
        ("Storage Organizer", "GOOD", "Keeps play area tidy, strong parental satisfaction"),
        ("Battery Mega-Pack", "OVERHYPED", "Often overbought — rechargeable is better value"),
        ("Off-brand Expansion Set", "AVOID", "Compatibility issues and lower build quality"),
        ("Gift Wrapping Service", "GOOD", "Low cost convenience for gifting"),
    ],
    "grocery": [
        ("Reusable Storage Bags", "GOOD", "Eco-friendly with high repeat usage"),
        ("Bulk Add-on Pack", "OVERHYPED", "Leads to waste if not consumed in time"),
        ("Premium Delivery Slot", "OVERHYPED", "Standard delivery is usually sufficient"),
    ],
    "automotive": [
        ("Installation Service", "GOOD", "Professional setup prevents costly errors"),
        ("Premium Wax Coating", "OVERHYPED", "Marginal benefit over standard options"),
        ("Unbranded Replacement Parts", "AVOID", "Safety and warranty voiding concerns"),
        ("Dash Cam Bundle", "GOOD", "High practical value for safety and insurance"),
    ],
    "health": [
        ("Carrying Pouch", "GOOD", "Convenient for daily portability"),
        ("Subscription Refill Plan", "OVERHYPED", "Often locks users into unwanted commitments"),
        ("Generic Alternative", "GOOD", "Same efficacy at lower cost — smart choice"),
        ("Unverified Supplements", "AVOID", "No regulatory approval — potential health risk"),
    ],
}

# Fallback bundle for unknown categories
DEFAULT_BUNDLE: list[tuple[str, str, str]] = [
    ("Protective Case", "GOOD", "General protection extends product lifespan"),
    ("Extended Warranty", "OVERHYPED", "Statistically rarely used by most buyers"),
    ("Third-party Accessories", "AVOID", "Quality and compatibility often unreliable"),
]


def generate_bundle(category: str) -> list[BundleItem]:
    """Return classified bundle items for the given product category."""
    cat = category.lower()
    raw = CATEGORY_BUNDLES.get(cat, DEFAULT_BUNDLE)
    return [
        BundleItem(name=name, label=label, reason=reason)
        for name, label, reason in raw
    ]
