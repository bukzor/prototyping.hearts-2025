# 2025-12-13: Initial Planning Session

## Focus

Requirements gathering and documentation structure for Hearts Online.

## What Happened

Extended discussion to clarify:
- Product vision (competitive Hearts, "fry or be fried")
- Target platforms (web, Android, iOS, Steam)
- Rules (standard + JD variant, shooter's choice for moon)
- Tech approach (Python POC → Rust production)
- Architecture (monorepo, separate packages)

Created full KB structure:
- 8 rules in `rules.kb/`
- 6 features in `features.kb/`
- 3 milestones in `milestones.kb/`
- 4 analogues in `tool-equivalence-classes.kb/`
- 6 ADRs in `dev/adr/`

## Decisions Made

See `dev/adr/2025-12-13-*.md` for formal records. Key ones:
- Python for POC, Rust for production
- FastAPI + htmx (no SPA complexity)
- No bots in ranked play (competitive integrity)
- Shooter's choice for moon shooting

## Next Session

**Start building a000-local-prototype:**

1. Set up uv workspace with packages: `engine`, `bot`, `server`
2. Implement core game engine (cards, hands, tricks, scoring)
3. Add basic bot (random legal play + simple heuristics)
4. Create FastAPI server with htmx frontend
5. Pass-the-controller UI: single browser, 4 players take turns

**Pass-the-controller mechanics:**
- One browser window shows current player's hand
- Other players look away or use honor system
- "End turn" button hides hand, prompts next player
- Good enough for playtesting, not production

**Success criteria:** Complete 4-player game to 100 points with correct rules.
