from __future__ import annotations

import pytest

from app.services.bias_analyzer import _mock_analyze, analyze_article_bias


class TestBiasAnalyzer:
    def test_mock_analyze_left_leaning(self) -> None:
        text = "This policy addresses systemic inequality and promotes equity and justice for marginalized communities."
        result = _mock_analyze(text)
        assert result.score < 0.0
        assert result.label in ["Center-Left", "Left"]

    def test_mock_analyze_right_leaning(self) -> None:
        text = "The free market approach to deregulation ensures fiscal responsibility and small government."
        result = _mock_analyze(text)
        assert result.score > 0.0
        assert result.label in ["Center-Right", "Right"]

    @pytest.mark.asyncio
    async def test_analyze_article_bias_empty(self) -> None:
        result = await analyze_article_bias(title="Short")
        assert result.score == 0.0
        assert result.label == "Center"
        assert result.confidence == 0.0

    @pytest.mark.asyncio
    async def test_analyze_article_bias_concatenates_fields(self) -> None:
        title = "A" * 15
        body = "B" * 15
        result = await analyze_article_bias(title=title, body=body)
        assert result.score is not None
        assert result.label is not None
