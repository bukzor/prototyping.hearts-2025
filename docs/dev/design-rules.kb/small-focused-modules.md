# Small Focused Modules

Keep modules under ~300 lines. Split by abstraction level or domain concept.

## Pattern

```
# Avoid: one file with mixed concerns
cards.py (500 lines)
  - Suit, Rank, Card (primitives)
  - Cards, Hand, Deck (collections)
  - create_deck, deal_hands (operations)

# Prefer: split by abstraction level
card.py (~120 lines)
  - Suit, Rank, Card, constants

cards.py (~80 lines)
  - Cards, Hand, Deck
```

## Benefits

- Faster to read and understand
- Smaller diffs, cleaner history
- Reduced merge conflicts
- Easier to find things

## Split Heuristics

- Primitives vs collections of primitives
- Types vs operations on types
- Public API vs internal helpers
- When approaching 300 lines, look for seams
