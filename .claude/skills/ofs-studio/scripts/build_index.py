#!/usr/bin/env python3
"""Rebuild the ofs-studio skill library index.

Reads every SKILL.md under .agents/skills (library) and .claude/skills (shelf),
sorts each skill into an OFS job category, and writes
.claude/skills/ofs-studio/library/<category>.md plus library/INDEX.md.

Run from the repository root after `npx skills add` or `npx skills update`:
    python3 -I .claude/skills/ofs-studio/scripts/build_index.py
SKILL.md files are third-party text: they are parsed as data, never executed.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / ".claude/skills/ofs-studio/library"
LOCK = ROOT / "skills-lock.json"

CATEGORIES = {
    "research-trends": ("Research, trends, scraping and competitor intel",
                        "Trend research, social listening, reel/ad teardowns, competitor and market research, web scraping."),
    "hooks-copy": ("Hooks, copy, captions and scripts",
                   "Hooks, ad copy, captions, social posts, email, long-form writing, editing and de-AI passes."),
    "video-motion": ("Video, motion, audio and AI generation",
                     "AI video models, HTML-to-video, motion graphics, editing, voiceover, music, SFX, 3D."),
    "image-design": ("Images, key art, brand and visual design",
                     "Posters, visual art, image generation and enhancement, brand guidelines, themes, diagrams."),
    "web-artifacts": ("Artifacts, pages, decks and front-end",
                      "Design direction and polish for HTML artifacts, landing pages, dashboards, slides, charts."),
    "marketing-growth": ("Marketing, ads, SEO and growth",
                         "Campaign strategy, paid ads, SEO/AEO, local SEO, CRO, launches, lead gen, sales enablement."),
    "strategy-business": ("Strategy, product and business operations",
                          "Positioning, pricing, business models, founder and C-suite advisors, finance, ops, meetings."),
    "planning-thinking": ("Planning, brainstorming and decision stress-tests",
                          "Brainstorming, interviews to sharpen a plan, pre-mortems, red-teaming, structured thinking."),
    "knowledge-base": ("Knowledge base, memory and notes",
                       "Obsidian vaults, wikis, knowledge graphs, capture and memory tools."),
    "engineering": ("Engineering, code quality, security and agent tooling",
                    "Coding workflows, reviews, debugging, security audits, MCP/skill building, Claude API."),
    "ai-ml-research": ("AI/ML research and infrastructure",
                       "Model training, fine-tuning, serving, evaluation, interpretability, vector stores."),
    "academic": ("Academic research and writing",
                 "Literature reviews, academic papers, systematic reviews, grants, patents."),
    "compliance": ("Compliance and regulated industries",
                   "ISO, SOC 2, GDPR, EU AI Act, FDA/MDR, QMS and audit readiness."),
    "terse-modes": ("Token-saving terse modes (never for client-facing work)",
                    "Caveman-style compressed replies and related tooling."),
    "misc": ("Other utilities and demos",
             "Small utilities, demo skills and one-off helpers."),
}

# Explicit placements win over the rules below.
OVERRIDES = {
    # research / trends
    **{n: "research-trends" for n in (
        "last30days", "agent-browser", "rea-video", "reverse-any-video", "autoresearch", "research",
        "defuddle", "content-research-writer", "competitive-ads-extractor", "lead-research-assistant",
        "youtube-downloader", "video-download", "video-understand", "customer-research", "competitors",
        "competitor-profiling", "reverse-engineer-marketing", "competitor-analysis", "market-sizing",
        "market-segments", "sentiment-analysis", "survey-design", "competitive-intel", "market-research",
        "product-research", "social-media-analyzer", "universal-scraping-architect", "dossier",
        "research-summarizer", "competitive-teardown", "source-audit", "competitor-alternatives",
        "browser-automation", "full-page-screenshot", "playwright-recording", "pulse", "linkedin-analytics",
        "campaign-analytics", "analytics", "interview-mapper", "user-personas", "customer-journey-map",
        "ml-autoresearch")},
    # hooks / copy
    **{n: "hooks-copy" for n in (
        "humanizer", "content-humanizer", "copywriting", "copy-editing", "ad-creative", "social", "emails",
        "email-sequence", "cold-email", "sms", "writing-beats", "writing-fragments", "writing-shape",
        "twitter-algorithm-optimizer", "social-content", "content-creator", "content-production",
        "x-twitter-growth", "linkedin-content", "linkedin-engagement", "linkedin-profile", "linkedin-skills",
        "linkedin-strategy", "doc-coauthoring", "internal-comms", "grammar-check", "email-template-builder",
        "release-notes", "md-document", "md-review", "contract-and-proposal-writer", "rfp-responder",
        "content-strategy", "youtube-full", "video-content-strategist", "internal-narrative",
        "team-communications", "public-relations")},
    # video / motion / audio
    **{n: "video-motion" for n in (
        "bang-motion", "cinematic-shot-prompting", "demo-video", "video-animatic", "video-beat-board",
        "video-conform", "video-director", "website-to-video", "flux-best-practices", "bfl-api", "comfyui",
        "3d-asset-generation", "game-universe-studio")},
    # image / brand / visual design
    **{n: "image-design" for n in (
        "algorithmic-art", "canvas-design", "theme-factory", "brand-guidelines", "brand-guidelines-kit",
        "slack-gif-creator", "image-enhancer", "diagram-design", "design-system", "ui-design-system",
        "epic-design", "apple-hig-expert", "design-qa", "visual-style", "canvas")},
    # artifacts / pages
    **{n: "web-artifacts" for n in (
        "frontend-design", "impeccable", "unslop", "hallmark", "design-taste-frontend", "web-artifacts-builder",
        "artifacts-builder", "landing-page-generator", "landing", "tailwind-design-system",
        "web-design-guidelines", "framer-motion", "vercel-react-best-practices", "vercel-composition-patterns",
        "d3-viz", "beautiful-mermaid", "md-slides", "markdown-html-orchestrator", "presentation-structure",
        "presentation-styling", "webapp-testing", "a11y-audit", "slideshow", "board-deck-builder", "figma")},
    # planning / thinking
    **{n: "planning-thinking" for n in (
        "brainstorming", "writing-plans", "executing-plans", "grill-me", "grilling", "grill-with-docs",
        "think", "pre-mortem", "strategy-red-team", "stress-test", "challenge", "roast", "decide",
        "hard-call", "teach", "to-questionnaire", "wait-what", "brainstorm-ideas-new",
        "brainstorm-ideas-existing", "brainstorm-experiments-new", "brainstorm-experiments-existing",
        "brainstorm-okrs", "identify-assumptions-new", "identify-assumptions-existing",
        "prioritize-assumptions", "scenario-war-room", "adversarial-reviewer",
        "named-persona-adversarial-review", "office-hours", "fable-goal", "loop-me", "interview")},
    # knowledge base
    **{n: "knowledge-base" for n in (
        "graphify", "llm-wiki", "notebooklm", "capture", "remember", "memory-review", "memory-status",
        "promote", "reflect", "agent-memory", "memory-engineering", "context-engine", "knowledge-ops",
        "book-to-skill", "inbox-setup", "inbox-triage")},
    # misc / demos
    **{n: "misc" for n in (
        "time-skill", "weather-fetcher", "weather-svg-creator", "raffle-winner-picker",
        "tailored-resume-generator", "review-resume", "invoice-organizer", "file-organizer",
        "domain-name-brainstormer", "vibe-to-agentic-framework", "dummy-dataset", "live-polls", "live-qa",
        "syllabus", "spinning-up-deep-rl", "deep-learning-book")},
    # engineering odds and ends from content-heavy repos
    **{n: "engineering" for n in (
        "find-skills", "security-audit", "karpathy-guidelines", "mcp-builder", "claude-api", "academy-guide",
        "discernment-nudge", "connect", "connect-apps", "skill-share", "langsmith-fetch",
        "developer-growth-analysis", "changelog-generator", "setup-api-key", "provider-model-refresh",
        "provider-refresh-oct23", "agents", "code-review", "sql-queries", "intended-vs-implemented",
        "shipping-artifacts", "test-scenarios", "lean-build", "surgical-patch", "safe-refactor", "migration",
        "investigate-first", "verify-and-stop", "caveman-review", "caveman-explore", "cavecrew",
        "google-workspace-cli", "atlassian-admin", "atlassian-templates", "confluence-expert", "jira-expert",
        "ms365-tenant-manager", "snowflake-development", "stripe-integration-expert", "saas-scaffolder",
        "spec-to-repo", "code-to-prd", "security-guidance", "llm-cost-optimizer", "prompt-governance",
        "prompt-engineer-toolkit", "senior-prompt-engineer", "write-a-skill", "skill-retro", "skillopt-sleep",
        "claude-coach", "behuman", "zero-hallucination-coder", "karpathy-coder", "agent-harness",
        "agent-launcher-orchestrator", "run-without-you", "human-gate", "collab-proof", "grade-iterate",
        "stage-launch", "wrap-up", "workflow-builder", "loop-library")},
    "image": "image-design", "video": "video-motion", "social-media-manager": "marketing-growth",
    "csuite-chief-of-staff": "strategy-business", "meeting-insights-analyzer": "strategy-business",
    "coding-agent-rollout": "engineering",
    "academic-deep-research": "academic",
    "meta-research": "academic", "litreview": "academic", "grants": "academic", "patent": "academic",
    "clinical-research": "academic", "research-finance": "strategy-business", "research-ops-skills": "academic",
}

SOURCE_DEFAULT = {
    "Orchestra-Research/AI-Research-SKILLs": "ai-ml-research",
    "OpenMontageInc/OpenMontage": "video-motion",
    "heygen-com/hyperframes": "video-motion",
    "coreyhaines31/marketingskills": "marketing-growth",
    "phuryn/pm-skills": "strategy-business",
    "mattpocock/skills": "engineering",
    "obra/superpowers": "engineering",
    "DietrichGebert/ponytail": "engineering",
    "JuliusBrussee/caveman": "terse-modes",
    "AgriciDaniel/claude-obsidian": "knowledge-base",
    "Imbad0202/academic-research-skills": "academic",
    "ComposioHQ/awesome-claude-skills": "misc",
    "anthropics/skills": "engineering",
    "shanraisshan/claude-code-best-practice": "misc",
    "cloudflare/security-audit-skill": "engineering",
}

# Name rules for the big alirezarezvani collection (checked in order).
NAME_RULES = [
    (r"(iso\d|soc2|gdpr|dsgvo|fda|mdr-|qms|qmr|iso13485|capa|cmmc|cra-|dora|nis2|eu-ai-act|ai-act|aims-|"
     r"compliance|regulatory|risk-management|quality-|medical-device|information-security|isms|ra-qm|access-lifecycle)",
     "compliance"),
    (r"^(ceo|cfo|coo|cto|cmo|cpo|cro|chro|ciso|caio|cco|cdo|vpe|gc|general-counsel|chief)-|c-level|board|"
     r"founder|executive|boardroom|company-os|culture|org-health|strategic|ma-playbook|intl-expansion|"
     r"change-management|decision-logger|arquiteto|ai-decision|agent-decision|cross-eval|^brief$|^execute$|"
     r"^freeze$|^onboard$|post-?mortem|andreessen|weekly-review|deep-work|meetings|meeting-|finance|financial|"
     r"month-end|deal|saas-metrics|stock-analysis|business-|commercial|channel-economics|pricing|procurement|"
     r"vendor|capacity|process-mapper|partnerships|revenue|customer-success|support-ops|sales-engineer|"
     r"product-|roadmap|scrum|agile|senior-pm|pm-skills|experiment-designer|ux-researcher|investment",
     "strategy-business"),
    (r"seo|aeo|cro$|-cro|paid-ads|marketing|launch|referral|webinar|campaign|ab-test|analytics-tracking|"
     r"app-store|schema-markup|free-tool|local-seo|popup|paywall|signup|onboarding-cro|form-cro|business-name",
     "marketing-growth"),
    (r"^(senior-|aws-|azure-|gcp-|cloud-|kubernetes|helm|terraform|docker|ci-cd|api-|database|sql-|"
     r"observability|slo-|incident|threat|red-team|security|secrets|env-secrets|chaos|performance|tdd|"
     r"pr-review|code-|commit|codebase|monorepo|git-|dependency|feature-flags|i18n|mobile-release|migration|"
     r"migrate|rag-|mcp-|agent-|tech-|tc-tracker|focused-fix|self-eval|ship-gate|skill-|spec-driven|"
     r"runbook|embedded|interview-system|engineering|ai-security|red-green|browserstack|testrail|pw|coverage|"
     r"fix$|generate$|report$|extract$|setup$|hub-|agenthub|eval$|merge$|spawn$|ar-|autoresearch-agent|"
     r"self-improving|data-quality|statistical|session-handoff|handoff|chief-of-staff)", "engineering"),
]


def parse_frontmatter(text):
    """Return (name, description) from SKILL.md front matter without executing anything."""
    if not text.startswith("---"):
        return None, None
    end = text.find("\n---", 3)
    if end == -1:
        return None, None
    lines = text[3:end].splitlines()
    data, i = {}, 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", lines[i])
        if m and m.group(1) in ("name", "description"):
            key, val = m.group(1), m.group(2).strip()
            if val in ("|", ">", "|-", ">-", "|+", ">+", ""):
                block = []
                i += 1
                while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                    block.append(lines[i].strip())
                    i += 1
                val = " ".join(b for b in block if b)
                data[key] = val
                continue
            if len(val) >= 2 and val[0] in "'\"" and val[-1] == val[0]:
                val = val[1:-1]
            data[key] = val
        i += 1
    return data.get("name"), data.get("description")


def short(desc, limit=170):
    desc = re.sub(r"\s+", " ", (desc or "").replace("|", "/")).strip()
    if len(desc) <= limit:
        return desc
    cut = desc[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(",;:.-") + "…"


def categorize(name, source):
    if name in OVERRIDES:
        return OVERRIDES[name]
    if source == "alirezarezvani/claude-skills":
        for pattern, cat in NAME_RULES:
            if re.search(pattern, name):
                return cat
        return "misc"
    if name.startswith(("gsap-", "threejs-", "hyperframes", "remotion", "manim", "lottie", "video-",
                        "seedance", "kling", "ltx", "pika", "minimax", "music", "sound-", "text-to-speech",
                        "speech-to-text", "azure-", "elevenlabs", "fish-audio", "doubao", "dashscope", "lyria",
                        "acestep", "avatar", "heygen", "faceswap", "ffmpeg", "grok-media", "gemini-omni")):
        return "video-motion"
    if name.startswith(("caveman", "ultracave", "megacave")):
        return "terse-modes"
    if name.startswith(("wiki", "obsidian")):
        return "knowledge-base"
    if name.startswith(("ponytail",)):
        return "engineering"
    if name.startswith(("gtm-", "positioning", "value-prop", "ideal-customer", "competitive-battlecard",
                        "beachhead", "growth-loops", "north-star", "product-name", "marketing-")):
        return "marketing-growth"
    return SOURCE_DEFAULT.get(source, "misc")


def main():
    lock = json.loads(LOCK.read_text()).get("skills", {}) if LOCK.exists() else {}
    entries = []
    for tier, base in (("shelf", ROOT / ".claude/skills"), ("library", ROOT / ".agents/skills")):
        if not base.is_dir():
            continue
        for skill_md in sorted(base.glob("*/SKILL.md")):
            folder = skill_md.parent.name
            if folder == "ofs-studio":
                continue
            if tier == "library" and (ROOT / ".claude/skills" / folder).exists():
                continue  # linked onto the shelf; list it once
            name, desc = parse_frontmatter(skill_md.read_text(errors="replace"))
            source = lock.get(folder, {}).get("source")
            if folder == "graphify":
                source = "Graphify-Labs/graphify (graphify CLI)"
            entries.append({
                "folder": folder, "name": name or folder, "desc": short(desc), "tier": tier,
                "path": str(skill_md.relative_to(ROOT)), "source": source or "unknown",
                "category": categorize(folder, source),
            })

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.md"):
        old.unlink()
    by_cat = {c: [] for c in CATEGORIES}
    for e in entries:
        by_cat[e["category"]].append(e)

    for cat, items in by_cat.items():
        title, blurb = CATEGORIES[cat]
        lines = [f"# {title}", "", blurb, "",
                 "Shelf skills are in the skill list (invoke by name). Library skills are not: Read the SKILL.md",
                 "at the path shown and follow it, resolving relative paths from that skill's folder.", ""]
        for e in sorted(items, key=lambda x: x["folder"]):
            renamed = f" (upstream name: {e['name']})" if e["name"] != e["folder"] else ""
            tag = "shelf" if e["tier"] == "shelf" else "library"
            lines.append(f"- **{e['folder']}**{renamed} [{tag}] {e['desc']} `{e['path']}` ({e['source']})")
        (OUT / f"{cat}.md").write_text("\n".join(lines) + "\n")

    total = len(entries)
    idx = ["# OFS skill library index", "",
           f"{total} skills: {sum(e['tier'] == 'shelf' for e in entries)} on the shelf (`.claude/skills`, always listed) and "
           f"{sum(e['tier'] == 'library' for e in entries)} in the library (`.agents/skills`, read on demand).",
           "Open the category file for the job, pick the skill, then Read its SKILL.md.", "",
           "| Category | Skills | File |", "|---|---|---|"]
    for cat, items in by_cat.items():
        idx.append(f"| {CATEGORIES[cat][0]} | {len(items)} | `library/{cat}.md` |")
    idx += ["", "Rebuild after adding or updating skills:",
            "`python3 -I .claude/skills/ofs-studio/scripts/build_index.py` (run from the repo root)."]
    (OUT / "INDEX.md").write_text("\n".join(idx) + "\n")
    print(f"indexed {total} skills into {len(CATEGORIES)} categories")
    for cat, items in by_cat.items():
        print(f"  {cat}: {len(items)}")


if __name__ == "__main__":
    sys.exit(main())
