# OFS skill library index

847 skills: 7 on the shelf (`.claude/skills`, always listed) and 840 in the library (`.agents/skills`, read on demand).
Open the category file for the job, pick the skill, then Read its SKILL.md.

| Category | Skills | File |
|---|---|---|
| Research, trends, scraping and competitor intel | 43 | `library/research-trends.md` |
| Hooks, copy, captions and scripts | 38 | `library/hooks-copy.md` |
| Video, motion, audio and AI generation | 85 | `library/video-motion.md` |
| Images, key art, brand and visual design | 16 | `library/image-design.md` |
| Artifacts, pages, decks and front-end | 25 | `library/web-artifacts.md` |
| Marketing, ads, SEO and growth | 70 | `library/marketing-growth.md` |
| Strategy, product and business operations | 131 | `library/strategy-business.md` |
| Planning, brainstorming and decision stress-tests | 32 | `library/planning-thinking.md` |
| Knowledge base, memory and notes | 27 | `library/knowledge-base.md` |
| Engineering, code quality, security and agent tooling | 210 | `library/engineering.md` |
| AI/ML research and infrastructure | 97 | `library/ai-ml-research.md` |
| Academic research and writing | 11 | `library/academic.md` |
| Compliance and regulated industries | 33 | `library/compliance.md` |
| Token-saving terse modes (never for client-facing work) | 13 | `library/terse-modes.md` |
| Other utilities and demos | 16 | `library/misc.md` |

Rebuild after adding or updating skills:
`python3 -I .claude/skills/ofs-studio/scripts/build_index.py` (run from the repo root).
