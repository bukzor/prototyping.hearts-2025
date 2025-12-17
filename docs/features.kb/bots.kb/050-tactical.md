# 050: Tactical Bot

Opponent modeling. Moon awareness.

## Knows

Everything from 030, plus:

- Approximate opponent hand composition (inference from plays)
- Who is likely shooting the moon
- Game score context (who needs to avoid points)

## Does

**Moon detection:**

- Recognize when opponent is shooting
- Sacrifice to block (take one heart to stop moon)
- Recognize own moon opportunity

**Moon pursuit:**

- If shooting looks viable, switch to point-taking mode
- Abandon moon if blocked

**Score awareness:**

- Play more aggressively when behind
- Play conservatively when ahead
- Target the leader

## Doesn't

- Deep lookahead
- Optimal play calculation
- Learn from past games
