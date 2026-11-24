# Token-saving terse modes (never for client-facing work)

Caveman-style compressed replies and related tooling.

Shelf skills are in the skill list (invoke by name). Library skills are not: Read the SKILL.md
at the path shown and follow it, resolving relative paths from that skill's folder.

- **caveman** [library] Terse caveman voice: answer first, fluff gone, every technical fact kept. Use for /caveman, "caveman mode", "talk like caveman", "be brief", "less tokens". Stays on… `.agents/skills/caveman/SKILL.md` (JuliusBrussee/caveman)
- **caveman-commit** [library] Write a Conventional Commits message compressed to intent only. Use for "write a commit", "commit message", /commit or /caveman-commit. `.agents/skills/caveman-commit/SKILL.md` (JuliusBrussee/caveman)
- **caveman-compress** [library] Compress a memory file such as CLAUDE.md or a todo list into caveman format to save input tokens, keeping a readable backup. Sends the file's text to the configured… `.agents/skills/caveman-compress/SKILL.md` (JuliusBrussee/caveman)
- **caveman-discover** [library] Find and label every LLM workflow in the repository so Caveman Cloud groups spend by workflow instead of one bucket. Use for "discover workflows" or breaking LLM spend… `.agents/skills/caveman-discover/SKILL.md` (JuliusBrussee/caveman)
- **caveman-evidence-review** [library] Read-only review of Caveman Cloud evidence: cost, Cave Score, workflows, traces, latency, errors, routing, savings. Use when asked what Caveman found or where LLM spend… `.agents/skills/caveman-evidence-review/SKILL.md` (JuliusBrussee/caveman)
- **caveman-help** [library] Quick-reference card for the three caveman skills and their commands. Trigger: /caveman-help or "caveman help". `.agents/skills/caveman-help/SKILL.md` (JuliusBrussee/caveman)
- **caveman-learn** [library] Act on a Caveman learn report - review the ranked token sinks, apply cost-lowering fixes with per-edit consent, and report what those fixes returned. Use when asked to… `.agents/skills/caveman-learn/SKILL.md` (JuliusBrussee/caveman)
- **caveman-manage** [library] Inspect Caveman Cloud's experiment lifecycle and block unsafe execution. Use when asked to start, approve, cancel, promote or roll back a Caveman experiment. `.agents/skills/caveman-manage/SKILL.md` (JuliusBrussee/caveman)
- **caveman-optimize** [library] Turn a Caveman optimization observation into an operator-chosen candidate with a paired baseline evaluation. Use when asked to inspect or evaluate a Caveman optimization… `.agents/skills/caveman-optimize/SKILL.md` (JuliusBrussee/caveman)
- **caveman-setup** [library] Wire a repository through the Caveman Cloud gateway so every LLM request is measured, with no behavior change. Use for "set up caveman" or adding LLM spend observability. `.agents/skills/caveman-setup/SKILL.md` (JuliusBrussee/caveman)
- **caveman-stats** [library] Show recorded output and cache-read token usage and mode attribution for the current Claude Code session, or locate the host's native usage report. Trigger… `.agents/skills/caveman-stats/SKILL.md` (JuliusBrussee/caveman)
- **megacave** [library] Caveman in Classical Chinese: 文言文 register, far fewer characters, technical terms verbatim. Invoke only with /megacave or /caveman wenyan. Stays on until "stop caveman"… `.agents/skills/megacave/SKILL.md` (JuliusBrussee/caveman)
- **ultracave** [library] Caveman at maximum compression: fragments, one word when one word is enough, each fact once. Invoke only with /ultracave or /caveman ultra. Stays on until "stop caveman"… `.agents/skills/ultracave/SKILL.md` (JuliusBrussee/caveman)
