# Opening Frame Studios (OFS)

OFS makes AI films, reels, ads and key art that look like real footage, mainly for cafés, real estate, luxury and D2C brands, often with realistic Indian characters.

## Every task goes through the router

- For any content, research, design, pitch or artifact work, invoke the `ofs-studio` skill first and follow its pipeline.
- Lead with the user's own OFS skills: `ofs-reel`, `ofs-cinematic-playbook`, `ofs-key-art`, `ofs-ad-factory`, `ofs-indian-characters`, `reel-breakdown`, `bang-motion`, `humanizer` (listed as `anthropic-skills:<name>` in Claude Code).
- Research uses live sources: vidIQ, `last30days`, Firecrawl or `agent-browser`, CreatorBerry once connected, and Windsor or Metricool for OFS's own numbers.
- Artifacts and pages: `frontend-design`, then `impeccable`, then `unslop`.
- Run `humanizer` last on anything a client or audience will read.

## Where the skills are

- `.claude/skills/`: the shelf, always in the skill list (the router plus a few core skills).
- `.agents/skills/`: a library of 840 more skills from the install list, kept out of the skill list so it does not crowd out the OFS skills. Find one through `.claude/skills/ofs-studio/library/INDEX.md`, then Read its `SKILL.md` and follow it.
- `skills-lock.json` pins every source. See `SKILLS.md` for updating, duplicates and security notes.

## Rules

- Never invent metrics, trends or quotes. Every number needs a source link and a date; if a source is down, say so.
- Ask before spending credits, publishing, emailing or scheduling anything.
- Face swaps, voice clones and real likenesses only with documented consent.
- When the container blocks a site, use a connector (Firecrawl, vidIQ, CreatorBerry) or WebSearch and WebFetch instead.
