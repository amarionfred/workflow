---
name: ai-retrieval-engineering
description: "Build and evaluate retrieval-augmented ML systems and bounded code agents with traceable context, reproducible inference, caching, and resource measurements. Use for retrieval baselines, model interfaces, and research-system integration."
---

# AI and retrieval engineering

Define the input/output contract and information boundary before selecting a framework. Prefer a small inspectable pipeline when it answers the question. Model providers, embedding models, external indexes, and paid services remain subject to project choices and budget.

## Retrieval contract

Index only the allowed revision. Keep source identity, commit, path, chunk bounds, content hash, parser/chunker version, and any embedding-model revision. Specify how code, scenes, resources, symbols, and dependencies become retrieval units. Check duplicates, generated files, secrets, and answer-bearing future material.

Compare against a feasible lexical/simple baseline before crediting a complex retriever. Evaluate evidence availability and retrieval usefulness on development/validation tasks without injecting final answer labels. Diagnose missing coverage, poor ranking, truncation, stale indexes, or answer generation separately.

For a matched-context adaptation comparison, freeze and reuse retrieved content, ordering, truncation, and tool access. If queries depend on the model, record that it changes the information received: either freeze the queries or label the result as a whole-system comparison. Equal top-k is not equal context.

## Inference and agent contract

Record model/revision, tokenizer/template, prompt hash, sampling parameters, stop rules, tool actions, attempts, and tokens. Key caches by all result-affecting inputs, including revision, context, adapter, and decoding config. Make offline replay possible without leaking grading artifacts to the candidate generator.

Bound retries, patch attempts, time, and tool permissions before evaluation. Distinguish timeout, parser, environment, and model failures. Do not silently retry failures into successes or drop them from the denominator. Read-only inspections and idempotent operations may retry under the declared policy; external writes need explicit handling of duplicate side effects.

Measure warm versus cold latency, startup/loading, prefill/decoding where available, peak memory, throughput at declared batch/concurrency, and total preparation/inference cost. Preserve answer quality when benchmarking quantization or serving changes. A hosted API must not receive private sources or held-out artifacts contrary to project rules.

Deliver a runnable pipeline, context trace, validation outcomes, and remaining confounds. Use [experiment review](../ml-experiment-review/SKILL.md) for claims. [FAISS index guidance](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index) is an optional technical reference, not an adopted dependency.
