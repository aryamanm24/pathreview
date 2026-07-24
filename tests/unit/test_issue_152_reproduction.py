"""Reproduction for issue #152 — faithfulness checker can never mark short
claims as supported.

Issue: https://github.com/ascherj/pathreview/issues/152

These tests capture the reported bug in
``rag/evaluator/faithfulness_checker.py``. They assert the *correct* behavior,
so they currently FAIL against the buggy implementation and will pass once the
fix from Week 9 lands. Run just this file with:

    .venv/bin/pytest tests/unit/test_issue_152_reproduction.py -v
"""

import pytest

from rag.evaluator.faithfulness_checker import FaithfulnessChecker


@pytest.mark.unit
class TestIssue152Reproduction:
    """Short, fully-grounded claims must not score 0.0."""

    @pytest.fixture
    def checker(self) -> FaithfulnessChecker:
        return FaithfulnessChecker()

    def test_short_supported_claims_are_not_zero(self, checker: FaithfulnessChecker) -> None:
        """Exact snippet from the issue: two short claims, each fully supported
        by a context chunk, currently scores 0.0.
        """
        score = checker.check(
            "Knows Python. Knows SQL.",
            [{"text": "python expert"}, {"text": "sql expert"}],
        )
        # Both claims are supported by the context, so the score should be high.
        assert score > 0.5

    def test_single_meaningful_token_can_support_a_short_claim(
        self, checker: FaithfulnessChecker
    ) -> None:
        """A one-keyword claim that the context clearly backs up should count
        as supported, but the >=2 meaningful-overlap rule rejects it today.
        """
        assert checker._is_supported("Knows Python", "python expert") is True
