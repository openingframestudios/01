---
name: ofs-studio
description: Router for every Opening Frame Studios (OFS) job. Use first for any OFS reel, ad, AI film, key art, caption, hook, trend or competitor research, client pitch or strategy, and for any artifact, page or deck. Picks the pipeline, then runs the right OFS skills, connectors, plugin skills and library skills in order.
---

# OFS Studio router

Match the job to a pipeline below and run its steps in order. Skip a step only when it plainly does not apply, and say which steps you skipped. The user's own OFS skills hold the house style, so they lead and everything else supports them.

## What is available

- **OFS skills (the user's own, in their claude.ai account; shown as `anthropic-skills:<name>` in Claude Code):** `ofs-reel`, `ofs-cinematic-playbook`, `ofs-key-art`, `ofs-ad-factory`, `ofs-indian-characters`, `reel-breakdown`, `bang-motion`, `humanizer`, `deep-research`.
- **Connectors (run server-side, so the container's network limits do not apply):** vidIQ (YouTube, Instagram and TikTok research: `vidiq_instagram_tiktok_outlier_search`, `vidiq_outliers`, `vidiq_trending_videos`, `vidiq_keyword_research`, `vidiq_video_transcript`, `vidiq_watch_shortform_content`, `vidiq_tiktok_trending_sound_search`, `vidiq_score_title`, `vidiq_score_thumbnail`, `vidiq_comment_insights`), Metricool (scheduling, best time to post, analytics), Windsor.ai (organic analytics for Instagram, Facebook, TikTok, YouTube, LinkedIn, Threads, Google Business Profile), Gmail, Google Calendar, Google Drive, Google Docs and Google Sheets (scripts, briefs, content calendars), and Firecrawl (`firecrawl_search` for web search and `firecrawl_scrape` for one page are routine research; `firecrawl_agent` multi-site jobs and Alexandria provider lookups such as TikTok or Instagram data charge more credits, so ask first). CreatorBerry (video research and hook patterns) works once the user connects it at claude.ai/customize/connectors; check with ListConnectors.
- **Plugin skills in the session:** `social-media-skills:*` (hook-writer, reels-script, caption-writer, hashtag-strategy, trend-jacking, viral-reverse-engineering, competitor-analysis, content-calendar, batch-content-plan, analytics-and-reporting, thumbnail-design, kling, veo-3, nano-banana, ai-voiceover, suno and more), `marketing:*`, `marketing-psychology:*`, `founderos:*`.
- **Shelf skills (in the skill list):** `last30days`, `agent-browser`, `impeccable`, `frontend-design`, `unslop`, `security-audit`, `find-skills`.
- **Library (840 skills, not in the skill list):** start at `library/INDEX.md` (in this skill's folder), open the category file, then Read `.agents/skills/<name>/SKILL.md` and follow it. Resolve its relative paths from that skill's folder.

Use whatever subset exists in the current surface. In a claude.ai chat there is no `.agents/skills`; use the OFS skills, plugins and connectors there.

## Pipelines

### 1. Reel or short video (Instagram, TikTok, Shorts)
1. **Research, in parallel:** vidIQ outliers and trending for the niche and city; `last30days` on the topic (Reddit, X, YouTube, TikTok, HN); CreatorBerry hook patterns if connected; Windsor or Metricool for what worked on OFS's own accounts. Note the top hooks, formats, lengths and sounds with links.
2. **Teardown of 1 to 3 references:** `reel-breakdown` (it drives the `rea-video` CLI; library `rea-video` has the commands). Library `reverse-any-video` rebuilds a reference as an editable HyperFrames project.
3. **Angle and hook:** `social-media-skills:hook-writer`, library `ad-creative` for an angle matrix, `marketing-psychology:evidence-check` for any psychology claim.
4. **Script and shots:** `ofs-reel` owns the end-to-end plan. Pair it with `ofs-cinematic-playbook` for shots, lenses, light, prompts and The Test, and with `ofs-indian-characters` whenever people appear.
5. **Motion, captions and audio:** `bang-motion` is the default for motion graphics. Library `hyperframes` (with `hyperframes-registry`, `media-use`) handles HTML-rendered video and captions. OpenMontage library skills cover the rest: `video-edit`, `video-toolkit`, `text-to-speech`, `elevenlabs`, `music`, `sound-effects`, `ffmpeg`.
6. **Caption and tags:** `social-media-skills:caption-writer` and `hashtag-strategy`, then a `humanizer` pass.
7. **Publish:** Metricool `createScheduledPostForReview` only. Never publish without the user's go-ahead.

### 2. Ads and spec ads for leads
1. Research the business and its competitors: Google Maps listing, reviews and site via Firecrawl or `agent-browser`; competitor ads via library `competitive-ads-extractor`; vidIQ for category outliers.
2. Angles: library `ad-creative` and `offers`, `marketing-psychology:persuasion-audit` on the draft.
3. Production: `ofs-ad-factory` (Higgsfield: Seedance, Kling, Marketing Studio, DTC Ads, Virality Predictor), `ofs-cinematic-playbook` for film quality, `ofs-key-art` for statics.
4. Copy: library `copywriting` and `copy-editing`, then `humanizer`.
5. Outreach for the lead: library `cold-email` or `prospecting`; `marketing-psychology:dark-pattern-check` before anything with urgency, pricing or trials.

### 3. Key art, posters, covers and statics
`ofs-key-art` leads (text-free AI plate, exact type and logo in HTML, rendered to PNG). Support: library `image` and `canvas-design` for direction, `flux-best-practices` or `social-media-skills:nano-banana` for the plate, `image-enhancer` for upscaling, `brand-guidelines-kit` when a client has no brand book, `social-media-skills:thumbnail-design` for covers.

### 4. AI film or brand film
`ofs-cinematic-playbook` (beat sheet, shot list, prompt templates, sound layers, AI-look fixes) with `ofs-indian-characters` for people. Model skills from the library: `kling-official`, `seedance-2-0`, `seedance-2-5`, `ltx2`, `minimax-h3`, `ai-video-gen`; plugin `social-media-skills:veo-3` and `kling`. Planning aids: library `video-director`, `video-beat-board`, `video-animatic`, `cinematic-shot-prompting`. Audio: `lyria`, `music-to-video`, `sound-effects`, `elevenlabs`.

### 5. Trend, competitor and market research
`last30days` for what people are saying now; vidIQ for what is performing; library `social-media-analyzer`, `competitor-profiling`, `reverse-engineer-marketing`, `customer-research`, `market-research`; `deep-research` (the user's) for a cited report; library `autoresearch` for a bounded research loop. Scrape pages with Firecrawl or `agent-browser`. Every number gets a source link and a date.

### 6. Client pitch, proposal or strategy
`social-media-skills:brand-profile` and `audience-research` to frame the client, `marketing:competitive-brief`, library `positioning-ideas`, `value-prop-statements`, `pricing-strategy`, `contract-and-proposal-writer`; `founderos:customer-proxy` or library `strategy-red-team` to stress-test; deliver as a doc or deck.

### 7. Artifacts, pages, dashboards and decks
`frontend-design` for direction, then `impeccable` for craft, and `unslop` last to remove AI tells. For websites, library `hallmark` or `design-taste-frontend` can replace the first step. Diagrams: library `diagram-design`. Charts: `dataviz`. Slides: the Slides artifact type, or library `md-slides`.

### 8. Any client-facing words
Run `humanizer` last on every caption, script, email and page. Library `writing-shape` helps with long-form structure.

### Vague brief or new campaign
Run library `brainstorming` (superpowers) or `grill-me` first to pin down goal, audience, offer and deliverable, then pick the pipeline.

## Rules

- **No invented data.** Views, engagement, prices, follower counts and trends come from a tool result or a cited page, with its date. If a source is unavailable, say so; do not fill the gap.
- **Ask first** before anything that spends credits (CreatorBerry analyses, ScrapeCreators, Higgsfield or other paid generations), publishes, emails, or schedules.
- **Consent:** face swaps, voice clones and real people's likeness only with documented consent.
- **Third-party data:** library `caveman-setup`, `caveman-compress`, `connect`, `connect-apps` and `skill-share` send content to outside services. Use them only when the user explicitly asks.
- **Terse modes** (`caveman`, `ultracave`, `megacave`) are never used for client-facing work.
- **Network:** the cloud container only reaches the hosts its environment allows. When a web request is blocked, switch to a connector (Firecrawl, vidIQ, CreatorBerry) or WebSearch and WebFetch rather than reporting no results.
- **Library upkeep:** after `npx skills add` or `npx skills update`, rebuild the index with `python3 -I .claude/skills/ofs-studio/scripts/build_index.py` from the repo root.
