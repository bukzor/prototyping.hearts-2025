--- # workaround: anthropics/claude-code#13003
requires:
    - Skill(llm.kb)
    - Skill(llm-collab)
---

# Hearts Game Documentation

Knowledge base for an online multiplayer Hearts game targeting competitive players.

## Structure

- `rules.kb/` - Hearts game rules, standard and optional variants
- `rust-python-analogues.kb/` - Mappings between Python POC and eventual Rust implementation
- `features.kb/` - Features to build (matchmaking, leaderboards, chat, etc.)
- `milestones.kb/` - Development milestones with alpha/beta/stable prefixes
- `dev/adr/` - Architecture Decision Records (date-based, per llm-collab)

## Milestone Naming

- `aNNN-$SLUG` - alpha (family only)
- `bNNN-$SLUG` - beta (friends)
- `vNNN-$SLUG` - stable (public)

## Principles

- Small focused files over large documents
- Frontmatter for structured metadata when useful
- `ls` for discovery, CLAUDE.md for maintenance guidance
