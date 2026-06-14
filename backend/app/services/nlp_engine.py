"""NLP Pipeline — Summarization and Zero-shot classification (SDG)."""

from __future__ import annotations

import logging
from typing import List, Optional

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

HF_INFERENCE_URL = "https://api-inference.huggingface.co/models"
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"

SDG_LABELS = [
    "SDG 7: Affordable and Clean Energy",
    "SDG 13: Climate Action",
    "SDG 9: Industry, Innovation and Infrastructure",
    "SDG 11: Sustainable Cities and Communities",
    "SDG 12: Responsible Consumption and Production",
]


async def _hf_summarize(text: str, token: str) -> Optional[str]:
    headers = {"Authorization": f"Bearer {token}"}
    truncated = text[:2000]  # HF inference API limits

    async with httpx.AsyncClient(timeout=45.0) as client:
        try:
            resp = await client.post(
                f"{HF_INFERENCE_URL}/{SUMMARIZATION_MODEL}",
                headers=headers,
                json={"inputs": truncated, "parameters": {"max_length": 130, "min_length": 30}},
            )
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("summary_text")
            logger.warning("HF summarize failed: %s", resp.text)
        except Exception as e:
            logger.error("HF summarize exception: %s", e)
    return None


async def _mock_summarize(text: str) -> str:
    """Fallback simplistic summarization."""
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 10]
    if not sentences:
        return "No summary could be generated."
    
    # Grab the first two meaningful sentences
    summary = ". ".join(sentences[:2]) + "."
    return f"[MOCK AI] {summary}"


async def generate_summary(text: str) -> str:
    if not text or len(text.strip()) < 50:
        return "Content too short to summarize."

    settings = get_settings()
    if settings.HF_API_TOKEN:
        summary = await _hf_summarize(text, settings.HF_API_TOKEN)
        if summary:
            return summary

    return await _mock_summarize(text)


async def _hf_zero_shot(text: str, token: str, candidate_labels: List[str]) -> List[str]:
    headers = {"Authorization": f"Bearer {token}"}
    truncated = text[:1000]

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(
                f"{HF_INFERENCE_URL}/{ZERO_SHOT_MODEL}",
                headers=headers,
                json={"inputs": truncated, "parameters": {"candidate_labels": candidate_labels}},
            )
            if resp.status_code == 200:
                data = resp.json()
                scores = data.get("scores", [])
                labels = data.get("labels", [])
                
                # Keep labels with score > 0.4
                matched = [labels[i] for i, s in enumerate(scores) if s > 0.4]
                return matched
            logger.warning("HF zero-shot failed: %s", resp.text)
        except Exception as e:
            logger.error("HF zero-shot exception: %s", e)
    return []


async def _mock_sdg_mapping(text: str) -> List[str]:
    """Fallback simplistic keyword matching for SDGs."""
    text_lower = text.lower()
    matched = set()
    
    if any(k in text_lower for k in ["solar", "wind", "renewable", "energy", "grid"]):
        matched.add("SDG 7: Affordable and Clean Energy")
    if any(k in text_lower for k in ["climate", "emission", "carbon", "warming", "greenhouse"]):
        matched.add("SDG 13: Climate Action")
    if any(k in text_lower for k in ["infrastructure", "industry", "manufacturing", "supply chain"]):
        matched.add("SDG 9: Industry, Innovation and Infrastructure")
        
    return list(matched)


async def map_sdgs(text: str) -> List[str]:
    if not text or len(text.strip()) < 20:
        return []

    settings = get_settings()
    if settings.HF_API_TOKEN:
        tags = await _hf_zero_shot(text, settings.HF_API_TOKEN, SDG_LABELS)
        if tags:
            return tags

    return await _mock_sdg_mapping(text)
