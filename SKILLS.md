# OFS skills setup

Everything from the install list is in this repo. Claude Code sessions on this repo load it automatically; `CLAUDE.md` sends every content, research and design task through the `ofs-studio` router.

## Two tiers

| Tier | Folder | Count | Visible to Claude |
|---|---|---|---|
| Shelf | `.claude/skills/` | 8 | Always, in the skill list |
| Library | `.agents/skills/` | 840 | On demand, through the router's index |

Why two tiers: Claude Code gives skill descriptions about 1% of the context window (roughly 8,000 characters on a 200k model). 847 skills would need about 180,000, so most would be cut to a bare name or dropped, including the OFS skills. Keeping the library out of the list leaves room for the skills that matter, and the router reaches the rest when a job needs them.

Shelf: `ofs-studio` (router), `last30days`, `agent-browser`, `impeccable`, `frontend-design`, `unslop`, `security-audit`, `find-skills`.

To move a library skill onto the shelf: `npx skills add <owner/repo> --skill <name> -a claude-code -y`, then rebuild the index.

## Sources (skills installed)

| Repo | Skills | Notes |
|---|---|---|
| alirezarezvani/claude-skills | 378 | 19 duplicates skipped; `brand-guidelines` installed as `brand-guidelines-kit`, `chief-of-staff` as `csuite-chief-of-staff` |
| Orchestra-Research/AI-Research-SKILLs | 98 | `autoresearch` installed as `ml-autoresearch` |
| OpenMontageInc/OpenMontage | 85 | 5 HyperFrames copies skipped (official versions installed); 2 upstream skills skipped by the installer for broken YAML |
| phuryn/pm-skills | 70 | `code-review` (a stub) and `marketing-ideas` skipped |
| coreyhaines31/marketingskills | 53 | Wins all marketing name clashes |
| mattpocock/skills | 38 | `retro` skipped (pm-skills version kept) |
| JuliusBrussee/caveman | 22 | |
| ComposioHQ/awesome-claude-skills | 19 | 9 copies of Anthropic skills skipped |
| obra/superpowers | 15 | includes `brainstorming` |
| AgriciDaniel/claude-obsidian | 15 | |
| anthropics/skills | 14 | docx, pdf, pptx, xlsx, skill-creator skipped: already in the claude.ai account |
| heygen-com/hyperframes | 9 | |
| DietrichGebert/ponytail, shanraisshan/claude-code-best-practice | 6 each | |
| Imbad0202/academic-research-skills | 5 | its `deep-research` differs from the account's `deep-research` |
| Single skills | 1 each | pbakaus/impeccable, Nutlope/hallmark, Leonxlnx/taste-skill, cathrynlavery/diagram-design, multica-ai/andrej-karpathy-skills, JuneYaooo/rea-video, blader/humanizer, mvanhorn/last30days-skill, bangtutorial/bang-motion, vercel-labs/skills (find-skills), vercel-labs/agent-browser, heydamir/unslop, cloudflare/security-audit-skill |
| Graphify-Labs/graphify | 1 | Not an npx package: installed with `graphify install --project --platform agents` (skill only, no hooks) |

`humanizer`, `bang-motion` and `karpathy-guidelines` are already in the claude.ai account; the library copies are the upstream originals and the router uses the account versions.

## Updating

```bash
npx skills update -p -y                                   # update every pinned skill
python3 -I .claude/skills/ofs-studio/scripts/build_index.py   # rebuild the router index
```

## Cloud environment

Run OFS sessions on the `openingframestudios-01` cloud environment. Cloud containers start fresh, and its setup script installs the CLIs below in each new one. The `Default` environment has no setup script and blocks every host in the table, so a session that starts there has none of this.

| Allowed host | Needed for |
|---|---|
| `www.reddit.com`, `arctic-shift.photon-reddit.com` | last30days Reddit |
| `hn.algolia.com` | last30days Hacker News |
| `gamma-api.polymarket.com` | last30days Polymarket |
| `www.youtube.com` | last30days YouTube, through yt-dlp |
| `www.modelscope.cn`, `cdn-lfs-cn-1.modelscope.cn` | rea-video OCR models for `--ocr-lang en`, `ja` and `ko` (the first redirects downloads to the second) |

GitHub, npm and PyPI work without being listed. Every other site stays blocked, so agent-browser can only reach these hosts; use Firecrawl for anything else.

If a session starts on `Default`, move it with `switch_environment` and install the CLIs by hand. A switch changes only the network: the setup script runs only when a fresh container starts.

### CLIs some skills need

- `agent-browser` (`npm i -g agent-browser`). Skip `agent-browser install` in the cloud container: its Chrome download is blocked there, and agent-browser already uses the container's Chromium through `CHROME_PATH`
- `yt-dlp` and `rea-video` (`uv tool install yt-dlp`, `uv tool install "rea-video[ocr] @ git+https://github.com/JuneYaooo/rea-video"`)
- `graphify` (`uv tool install graphifyy`)

### Known gaps

- rea-video's face model download gets a 403 from github.com even though GitHub is allowed, so face detection falls back to OpenCV's older Haar detector.
- Without the two ModelScope hosts, `rea-video --ocr-lang en` finds no on-screen text yet still reports success. The default OCR model ships inside the package and reads English too.
- rea-video has no vision model configured, so it tells live action, AI and 3D apart from pixel statistics alone. `rea-video review` lets Claude look at the frames instead, with no key needed.
- last30days covers TikTok and Instagram only through its keyless yt-dlp fallback, which finds less, and X is off. Turning them on needs keys that cost credits past a free tier, so ask first.

## Setup check (24 Nov 2026)

Checked from a fresh cloud session. The repo checks out: all 847 skills have valid front matter, the index rebuilds with no changes, and every skill the router names exists. Still open on the account side:

- Metricool is signed in, but its brand has no social account, so scheduling, best time to post and analytics have nothing to work with.
- Windsor sees the `openingframestudios` Instagram account with 0 followers and 0 posts (Windsor `get_data`, 24 Nov 2026). Reconnect it if the account has posts. Windsor is on a trial plan.
- CreatorBerry is not connected.
- vidIQ is signed in with no YouTube channel linked. Its Instagram and TikTok research works without one.
- The marketing plugin's own servers (Ahrefs, Canva, Figma, Notion, Slack and others) can't connect from the container. No OFS pipeline uses them.
- The OFS skills show in the skill list by name only: the plugins load about 190 skills, which uses up the description budget. The router names each OFS skill, so only automatic triggering suffers. `SLASH_COMMAND_TOOL_CHAR_BUDGET` raises the budget (untested).

## Security review (24 Nov 2026)

Automated scan of all 847 skills plus spot checks. Nothing malicious found: no hidden webhooks or paste/tunnel endpoints, no obfuscated code, no pipe-to-shell installers, no prompt-injection phrasing outside security documentation.

Worth knowing:

- `last30days` grants itself Bash while it runs, and with keys configured it sends search queries to ScrapeCreators, X, xAI, OpenAI or others it lists.
- `caveman-setup` routes LLM traffic through Caveman Cloud and tells the agent to send a verification request without asking; `caveman-compress` sends a file's full text to a model provider; Composio's `connect`, `connect-apps` and `skill-share` go through Composio. The router only uses these on an explicit request.
- `design-taste-frontend` declares a Stop hook that runs its local `gate.mjs` check. It only runs if that skill is moved onto the shelf.
- `gemini-omni` and `seedance-2-0` grant themselves Bash while active.
- superpowers' brainstorming companion page loads a logo from primeradiant.com; set `SUPERPOWERS_DISABLE_TELEMETRY=1` to stop it.
- The `skills` CLI sends anonymous install telemetry to its maintainers.
