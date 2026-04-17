"""FastAPI application — Retail AI Decision Engine."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import ProductRequest, AnalysisResponse
from logic.scoring import compute_score, score_to_decision
from logic.risk import assess_regret_risk
from logic.bundle import generate_bundle
from services.gemini import generate_explanation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalysisResponseWithBreakdown(AnalysisResponse):
    score_breakdown: dict[str, int]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Retail AI Decision Engine started")
    yield
    logger.info("👋 Shutting down")


app = FastAPI(
    title="Retail AI Decision Engine",
    description="AI-powered purchase decision API — BUY / WAIT / SKIP",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow frontend to connect from any origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze", response_model=AnalysisResponseWithBreakdown)
async def analyze_product(product: ProductRequest):
    """
    Analyze a product and return a structured purchase decision.

    Pipeline:
      1. Score the product using rule-based heuristics
      2. Map score → decision (BUY / WAIT / SKIP)
      3. Assess regret risk
      4. Generate category-specific bundle recommendations
      5. Call Gemini for a natural language explanation
    """
    try:
        # Step 1-2: Score and decide
        score, factors, score_breakdown = compute_score(product)
        decision = score_to_decision(score)

        # Step 3: Regret risk
        regret_risk = assess_regret_risk(product, score)

        # Step 4: Bundle
        bundle = generate_bundle(product.category)

        # Step 5: AI explanation
        ai_explanation = await generate_explanation(
            product=product,
            decision=decision,
            confidence=score,
            regret_risk=regret_risk,
            factors=factors,
            bundle=bundle,
        )

        return AnalysisResponseWithBreakdown(
            decision=decision,
            confidence=score,
            regret_risk=regret_risk,
            factors=factors,
            bundle=bundle,
            ai_explanation=ai_explanation,
            score_breakdown=score_breakdown,
        )

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "retail-ai-decision-engine"}
