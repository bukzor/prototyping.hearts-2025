# 030: Counting Bot

Tracks cards played. Knows what's out.

## Knows

Everything from 010, plus:

- Cards played this round
- Which suits are exhausted per player
- Whether Q♠ has been played
- Points taken per player this round

## Does

**Passing:**

- Void short suits strategically
- Keep low cards in long suits

**Playing:**

- Lead suits opponents are void in (to bleed points)
- Know when Q♠ is "safe" to lead
- Take tricks when no points remain

**Blocking:**

- Don't give free void to dangerous player

## Doesn't

- Predict opponent hands
- Calculate probabilities
- Simulate futures
