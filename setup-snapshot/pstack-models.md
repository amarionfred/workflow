# pstack model configuration for Codex

All roles: inherit-parent.
Panels: independent contexts on the parent model unless the user explicitly requests available different models.
Concurrency: obey the live tool limit; divide work only when it can run independently.
Reasoning: inherit the session setting. This installation currently defaults to gpt-6-astra with xhigh reasoning.

This preserves the user's current model choice without requiring Grok or Claude accounts. Change role allocations only when a real workload or user preference justifies it. Budget is a resource constraint, not a reason to weaken the definition of done.
