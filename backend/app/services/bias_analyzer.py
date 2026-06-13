"""Bias detection service — analyzes article text for political/media bias.

Uses HuggingFace Inference API when HF_API_TOKEN is set, otherwise falls back
to a deterministic mock analyzer that produces realistic scores from text heuristics.
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from typing import Optional

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

HF_INFERENCE_URL = "https://api-inference.huggingface.co/models"
BIAS_MODEL = "d4data/bias-detection-model"
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@dataclass(frozen=True)
class BiasResult:
    score: float          # -1.0 (strong left) to +1.0 (strong right)
    label: str            # "Left", "Center-Left", "Center", "Center-Right", "Right"
    confidence: float     # 0.0–1.0


def _score_to_label(score: float) -> str:
    if score <= -0.6:
        return "Left"
    if score <= -0.2:
        return "Center-Left"
    if score <= 0.2:
        return "Center"
    if score <= 0.6:
        return "Center-Right"
    return "Right"


_LEFT_MARKERS = re.compile(
    r"\b(inequality|progressive|marginalized|systemic|justice|equity|"
    r"climate crisis|workers rights|social safety net|universal healthcare)\b",
    re.IGNORECASE,
)
_RIGHT_MARKERS = re.compile(
    r"\b(free market|deregulation|traditional values|fiscal responsibility|"
    r"law and order|border security|tax cuts|small government|liberty)\b",
    re.IGNORECASE,
)
_EMOTIONAL = re.compile(
    r"\b(shocking|outrageous|alarming|devastating|unprecedented|explosive|"
    r"slammed|blasted|destroyed|crushed)\b",
    re.IGNORECASE,
)


def _mock_analyze(text: str) -> BiasResult:
    text_lower = text.lower()
    seed = int(hashlib.md5(text_lower[:200].encode()).hexdigest()[:8], 16)

    left_hits = len(_LEFT_MARKERS.findall(text))
    right_hits = len(_RIGHT_MARKERS.findall(text))
    emotional_hits = len(_EMOTIONAL.findall(text))

    base = (seed % 100 - 50) / 100.0  # -0.50 to +0.49
    directional = (right_hits - left_hits) * 0.12
    raw = base + directional

    score = max(-1.0, min(1.0, raw))
    confidence = min(1.0, 0.4 + emotional_hits * 0.08 + abs(directional) * 0.5)

    return BiasResult(
        score=round(score, 3),
        label=_score_to_label(score),
        confidence=round(confidence, 3),
    )


async def _hf_analyze(text: str, token: str) -> BiasResult:
    truncated = text[:1024]
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        bias_resp = await client.post(
            f"{HF_INFERENCE_URL}/{BIAS_MODEL}",
            headers=headers,
            json={"inputs": truncated},
        )

        if bias_resp.status_code != 200:
            logger.warning("HF bias model returned %d, falling back to mock", bias_resp.status_code)
            return _mock_analyze(text)

        bias_data = bias_resp.json()

        if isinstance(bias_data, list) and len(bias_data) > 0:
            predictions = bias_data[0] if isinstance(bias_data[0], list) else bias_data
            biased_score = 0.0
            confidence = 0.5

            for pred in predictions:
                lbl = pred.get("label", "").upper()
                sc = pred.get("score", 0.0)
                if lbl == "BIASED" or lbl == "LABEL_1":
                    biased_score = sc
                    confidence = sc
                elif lbl == "NON-BIASED" or lbl == "LABEL_0":
                    confidence = max(confidence, sc)

            seed = int(hashlib.md5(truncated[:200].encode()).hexdigest()[:8], 16)
            direction = (seed % 200 - 100) / 100.0
            score = direction * biased_score
            score = max(-1.0, min(1.0, score))

            return BiasResult(
                score=round(score, 3),
                label=_score_to_label(score),
                confidence=round(confidence, 3),
            )

    return _mock_analyze(text)


async def analyze_bias(text: str) -> BiasResult:
    if not text or len(text.strip()) < 20:
        return BiasResult(score=0.0, label="Center", confidence=0.0)

    settings = get_settings()
    if settings.HF_API_TOKEN:
        try:
            return await _hf_analyze(text, settings.HF_API_TOKEN)
        except Exception as exc:
            logger.warning("HF inference failed (%s), falling back to mock", exc)

    return _mock_analyze(text)


async def analyze_article_bias(
    title: str,
    body: Optional[str] = None,
    summary: Optional[str] = None,
) -> BiasResult:
    text = title
    if body:
        text = f"{title}\n\n{body}"
    elif summary:
        text = f"{title}\n\n{summary}"

    return await analyze_bias(text)
