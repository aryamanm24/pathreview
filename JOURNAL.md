# PathReview — Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/152

**Issue title:** Faithfulness checker can never mark short claims as supported

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The RAG faithfulness evaluator (`rag/evaluator/faithfulness_checker.py`) scores
generated feedback by checking how many of its individual claims are actually
"supported" by the retrieved context chunks. The bug lives in `_is_supported()`,
which only counts a claim as supported when it shares at least two meaningful
(non-stopword) tokens with the context. Short but fully grounded claims such as
"Knows Python." share just one meaningful token with a context that plainly
supports them, so they are always marked unsupported and the overall score
collapses to 0.0. A successful fix makes the support check scale to the length of
the claim — so a genuinely covered one-keyword claim can still count as supported
— while still rejecting claims the context does not actually back up, which
restores an accurate faithfulness score and makes the three related tests in
`tests/unit/test_faithfulness_checker.py` pass.

**Branch name:** fix/152-faithfulness-short-claim-support

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

### Selection notes — "Is this right for me?" reasoning

- **Scope is contained:** The fix is limited to a single function (`_is_supported()`)
  in one file (`rag/evaluator/faithfulness_checker.py`). No cross-module or
  database/API changes are required.
- **Clearly reproducible:** The issue provides an exact repro snippet and names the
  three failing unit tests (`test_partial_support_returns_middle_score`,
  `test_multiple_context_chunks`, `test_multiple_claims_varying_support`), so I have
  an objective definition of "done."
- **No heavy external dependencies:** The checker and its tests run purely in
  Python via `make test-unit` — they do not need the LLM provider or the ChromaDB
  vector service, so a fully green vector DB isn't a blocker for this issue.
- **Right difficulty level:** It's a Tier 1 bug, but it's a real logic fix (not a
  test-fixture tweak or one-line crash guard), so it forces me to understand how a
  RAG system verifies that feedback is grounded in evidence — good learning value
  for a first contribution.
- **Risk / unknowns:** The main judgment call is choosing the right supported-ness
  rule (e.g. scaling required overlap to claim length) so that short valid claims
  pass without making unrelated claims pass too. I'll validate that balance against
  the full `test_faithfulness_checker.py` suite before opening a PR.

**Environment status:** `make setup` and `make run` succeed; frontend confirmed
returning HTTP 200 at http://localhost:5173/ with the backend on :8000. (Note: the
`chromadb/chroma:0.4.22` container currently crashes on NumPy 2.0; not required for
issue #152 and can be addressed separately.)
