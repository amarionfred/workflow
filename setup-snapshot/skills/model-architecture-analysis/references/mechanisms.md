# Mechanism checks

| Mechanism | Inspect | Useful distinguishing control |
| --- | --- | --- |
| Attention | Q/K/V shapes, head mapping, causal/padding masks, positional representation, cache behavior | Same data and budget with a simpler attention/context policy |
| Recurrence or state-space memory | State size/update, reset/detach rules, padding, sequence boundaries, parallel versus step execution | Same effective history and matched state/memory budget where feasible |
| Mixture of experts | Router scores, top-k, total versus active parameters, load balance, capacity/drop behavior, communication | Dense control and matched active compute; disclose total capacity difference |
| External retrieval | Revision eligibility, query/ranking, evidence coverage, context budget | Freeze retrieved content when isolating learned-weight effects |
| Test-time learning | Which parameters/state update, label availability, reset policy, per-item compute | Frozen control with the same information and tuning allowance |
| Distillation/adaptation | Target source/objective versus trainable parameterization | Factor them separately instead of crediting architecture |

An architectural argument needs a chain: observed failure → candidate mechanism → falsifiable prediction → controlled intervention → repeated evidence. If only the first two exist, label a hypothesis. A synthetic mechanism demonstration does not establish repository-repair quality.

For interpretability, inspect intervention specificity, random/control interventions, baseline damage, and whether conclusions survive alternative readouts. Do not promote a visualization, attention map, or linear probe into a causal explanation.
