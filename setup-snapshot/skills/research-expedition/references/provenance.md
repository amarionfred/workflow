# Provenance and maintenance

Created for Game Model Research on 2026-10-04 by the assistant. These are project-informed procedural skills, not empirical claims that adding them improves research outcomes. All nine authored skills are local instructions; they are not official DeepMind or OpenAI research curricula.

The user asked to integrate [this X post](https://x.com/0xCarnagee/status/2090102148344262659), linking [the article](https://x.com/i/article/2090077664933449729). Direct X browsing returned 403. Article content and identifiers were recovered through the public FxTwitter API on 2026-10-04 and matched an accessible mirror. The article motivates role focus, persistent memory, reusable skill handoffs, evidence, and explicit boundaries. Its anecdotes, timing claims, product limits, and organizational attribution were not independently established and are not guarantees of this setup.

This adaptation uses the existing assistant runtime and the project's notebook. It does not install Grok, a scheduled watcher, a cloud team, or an autonomous training loop. Model/data choices and phase gates come from project instructions. Existing authorizations remain effective.

[Official skill documentation](https://learn.chatgpt.com/docs/build-skills) was checked for discovery and progressive loading. `jupyter-notebook` and `pdf` are separately sourced from `openai/skills`; their license and file-level provenance are retained in the installation manifest. Use their helper scripts only after inspection. For notebooks, pass an explicit project-approved output path rather than relying on the helper's skill-directory-relative default. Do not copy an example that reassigns `CODEX_HOME`; use a task-specific path variable.

[Orchestra Research](https://github.com/Orchestra-Research/AI-Research-SKILLs) and [AREX-Skill](https://github.com/VectorSpaceLab/AREX-Skill) were inspected at catalog level as extension sources. Their full contents and benchmark claims were not audited; neither library was installed. Select and inspect a narrowly relevant skill at a pinned revision when a concrete need arises. Do not import a whole catalog or trust performance claims as project evidence.

Maintenance: after a verified failure, change the smallest relevant instruction; record date, evidence, and reason in the canonical notebook. Validate frontmatter, local references, and scripts. For scientific methods, perform the task-specific empirical checks too. Link validation is not behavioral validation, and neither is a measured research result.
