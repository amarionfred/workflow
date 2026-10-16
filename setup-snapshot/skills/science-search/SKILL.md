---
name: science-search
description: "Search scholarly literature with ScienceMadeReadable: discover papers by meaning or exact terms, retrieve paper records, find similar work, and follow citations. Use for scientific evidence searches, literature reviews, and prior-work discovery, including ML research."
---

# Science search

Use the `science` MCP server at `https://api.sciencemadereadable.com/mcp`. It is a public, read-only service with no API key. Its [live guide](https://api.sciencemadereadable.com/api/data/llms.txt) documents current coverage and parameters; consult it when coverage or API details matter.

## Research workflow

- Use `search_papers` with a question phrased in research language. Choose `mode="semantic"` for concepts and `mode="keyword"` for exact titles, names, acronyms, or Boolean queries. For literature reviews, search both and deduplicate by OpenAlex ID; merge preprint/publication versions when appropriate.
- Screen with `abstracts="short"` or `"none"`, then use `get_papers` with shortlisted identifiers (up to 20) for complete metadata and abstracts. Supported identifiers include DOI, OpenAlex W-number, and PMCID.
- Expand promising leads with `find_similar_papers` and `citation_walk` when the question needs broader coverage.
- Open the primary paper or official repository before making claims about methods or results. Cite verified paper URLs/DOIs and state the reading depth. Search records and abstracts are discovery evidence, not a full-paper review.

The index covers English titles and abstracts, not full texts or literally all science. Semantic and keyword coverage differ; snapshot and daily updates can lag new papers or corrections. Supplement searches with primary publisher, preprint, or official repository sources when recency or coverage matters. Similarity, citation counts, topic labels, and junk scores are not evidence that a claim is correct.

## Limits and fallback

Make requests sequentially and stay within 30 calls per minute per address. Respect `Retry-After` or the tool's wait guidance; stop after two failed retries and use another source. Do not force Boolean matching through `mode="auto"` when exact terms are required: an empty keyword search can fall back to semantic search.

If MCP tools are unavailable in the current session, use the same public JSON API:

```sh
curl -L -sS --fail-with-body --max-time 45 --get \
  'https://api.sciencemadereadable.com/api/data/search' \
  --data-urlencode 'q=retrieval augmented generation' \
  --data-urlencode 'mode=semantic' \
  --data-urlencode 'k=10' \
  --data-urlencode 'abstracts=false'
```

For browser-only access, open `https://ask.sciencemadereadable.com/<URL-encoded question>?k=10`. Consult the live guide for record lookup, filters, and citation-walk endpoints. The service logs query text, so search with public research terms rather than private source material.
