# Confounds worth catching

| Observation | Review response |
| --- | --- |
| Adapted model repairs 8/10, base repairs 6/10 with different retrieved files | Describe an observed whole-system difference. Obtain matched permitted context before isolating training benefit; report pairing and small-sample limits |
| New method selected after repeatedly scoring the final set | Label selection contamination; do not keep claiming untouched final evaluation |
| Hundreds of tasks from one game have narrow task-bootstrap intervals | The interval does not establish generalization across games. Preserve task dependencies and state the actual sampling population |
| Static adapter works on later commits | Evidence about later-task usefulness; sequential retention/forgetting remains unmeasured |
| Provider charged no cash | Report consumed credits and gross usage separately; cash-free is not resource-free |
| Compilation passes | Behavioral repair unresolved until independent checks pass |
| Training loss falls on a tiny overfit check | Wiring check succeeded; adaptation benefit remains unmeasured |
| New architecture has higher score and twice the training budget | Separate architecture from resource allocation with a suitable control |
| Worker reviewed reference fixes, then produced candidate repairs in a new chat | Context/file access may contaminate generation; a new role label is not proof of blindness |

For every factor missing from the design, record why it is not measured, not a fabricated zero. Negative and infrastructure outcomes remain in the record with their correct status. Propose the smallest additional comparison, but do not silently authorize it.
