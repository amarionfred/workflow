# Working together

Your strongest contribution is deciding what deserves to exist, recognizing whether the result feels right, and explaining what matters. My role is to turn that direction into investigated, implemented, and checked work. You can speak naturally or use `/record`; polished prompt wording is optional.

Treat us like a director and a production team. You describe the scene's effect and its constraints. I determine the needed work, produce a version, and bring back something observable. You then give specific direction. That analogy breaks down when it suggests I can own your taste, infer unknown facts, or certify my own claims without evidence.

A useful brief gives six things: **outcome, context, constraints, proof, authority, and stopping condition**. Often three sentences cover them. Point to the canonical project record instead of pasting its entire history. Examples or screenshots of the desired result can carry more information than another paragraph of adjectives.

```text
In [project], make [observable outcome] work for [user/situation].
Read [entry point]. Preserve [constraints]; you may [authorized actions].
Done means [observable checks]. Continue through those checks, then explain
the result and remaining limits. Stop after [scope/time/compute boundary].
```

For a substantial or ambiguous task, add: “Restate the goal in your own words and tell me which assumption could most change the approach.” This catches a wrong interpretation before it becomes a large implementation. For a simple edit, just name the edit.

**For your prison game:**

```text
In Alcatraz, make the first corridor encounter teach the player to listen
before moving. Read the production handoff and the current encounter files.
Use the existing map and assets. Implement a playable slice, inspect it in
Studio, and capture the trigger, player warning, pursuit, and recovery.
You may change the relevant scripts and local place; do not publish.
Done means the encounter can be understood and recovered from on a first
playthrough. Explain which observations still require a human playtest.
```

This leaves room to solve the experience while defining the evidence. A screenshot can prove a composition; it cannot prove understandable pacing or comfortable camera motion. Use your existing horror, audio, first-person, and QA skills according to the changed surface.

**For your ML research:**

```text
Resume the active project from its canonical research record. Turn the
current claim about recurrent memory into one discriminating experiment.
Recover the approved model, dataset split, metric, compute limit, and
baseline. Implement missing evaluation plumbing first. Run only within
the existing budget, compare paired outcomes, and preserve raw results.
If a budget or experiment-defining decision is missing, make that specific
decision visible while continuing independent preparation.
```

Research needs a falsifiable claim and controls. A successful training run, an attractive plot, and a generated paper establish different things. Your existing research-expedition, experiment-review, architecture, retrieval, and training skills remain the main research discipline. Sakana supplies execution structure; it does not replace judgment about the experiment.

**For Orator or another app:**

```text
Reproduce [specific failure] from the real user flow. Preserve existing
voice behavior. Find the cause, implement the smallest durable fix, and
repeat the original flow plus the relevant regression checks. Keep a
before/after artifact. Do not stop after compilation.
```

**For work while you are away:**

```text
Work toward [bounded outcome]. You may edit, test, and create a draft PR.
Do not merge, publish, purchase, or message others. Use at most [resource
budget]. Keep a current handoff with exact process/job handles and evidence.
If one branch is blocked, continue authorized independent work. Stop when
the acceptance checks pass or the stated resource limit is reached.
```

Use an actual persistent Codex goal when you want continued pursuit. A new full-access session avoids approval prompts, but local work still needs the computer awake, its process running, connectivity, and plan capacity. A timer can catch up after login; it cannot run a powered-off laptop. A cloud runner would be a separate installation with its own credentials and resource limits.

When parallel agents would help, explicitly say: “Use parallel agents for independent investigations; give each a bounded deliverable and verify their output.” More agents can increase duplicated work, conflicting edits, and correlated mistakes. Parallelize independent uncertainty; keep shared decisions and integration owned.

The workflow has three loops:

1. **Choose the work:** retrieve context, identify the biggest uncertainty, define a useful result and a stop condition.
2. **Do the work:** inspect, implement, run the relevant check, repair failures, and repeat until the promised behavior holds.
3. **Improve the method:** examine actual failures and friction, change the structure that caused them, and check the change on later tasks.

Think of a thermostat: an objective, a sensor, an action, and feedback. If the sensor only measures whether the agent said “done,” the loop can confidently optimize the wrong thing. For a game use play behavior; for a service use the real request path; for research use controlled evaluation. A reviewer model provides another judgment, not independent ground truth.

Correct me with a concrete contrast: “The door should remain locked after reconnecting; this version forgets that state. Preserve server ownership and demonstrate reconnect behavior.” Then ask for the failure to become a regression check or a better data model. Use `$pstack:correct` when the failure suggests a general method problem. Avoid accumulating broad instructions from every isolated inconvenience.

Trust should expand by capability. Several successful code refactors support trusting that workflow more; they say little about deployment, game feel, or scientific novelty. Keep receipts for representative tasks, including failures. Review accepted outcomes, correction count, elapsed time, and measured cost where available. Compare similar tasks before asserting a productivity gain. Missing measurements remain unknown.

The Empryo setup trial illustrates this: its model produced the receipt summarizer and passed three tests. Our independent 22-case check caught two malformed-input failures. Codex corrected the boundary validation and preserved those regressions. That earns confidence in this small, reviewed function, not unrestricted confidence in every coding task.

Felix Rieseberg's ambition framework gives you four directions to explore: shorten delivery time, aim at a more consequential outcome, demand deeper evidence, or connect another discipline. Pick the useful direction for the project. For the corridor encounter, a larger ambition might combine sound, behavior, and recovery into one coherent player experience. For research, it might turn a vague architectural intuition into a decisive measurement. [Primary article](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).

For learning, say: “Explain the mechanism, ask me to predict one outcome, let me implement a small part, then review my result.” Use `$pstack:teach`, `$pstack:how`, and `$pstack:why` for explanations and the existing `ml-guided-learning` skill for research participation. Work I wrote stays attributed to me; your own implementation and explanation are what demonstrate your understanding.

Your first exercise: choose one unfinished project task and write three sentences using outcome, proof, and boundary. Before sending it, ask yourself: *Could I tell whether this succeeded without believing the agent's summary?* If the answer is no, improve the proof, not the wording.
