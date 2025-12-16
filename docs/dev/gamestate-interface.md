# GameState Interface

Renderer-agnostic contract between engine and renderer. See ADR-009.

## Core Types

```typescript
type Suit = "clubs" | "diamonds" | "hearts" | "spades";
type Rank =
  | "2"
  | "3"
  | "4"
  | "5"
  | "6"
  | "7"
  | "8"
  | "9"
  | "10"
  | "J"
  | "Q"
  | "K"
  | "A";

interface Card {
  suit: Suit;
  rank: Rank;
}

type PlayerId = 0 | 1 | 2 | 3;

interface Play {
  player: PlayerId;
  card: Card;
}
```

## GameState (Engine → Renderer)

```typescript
interface GameState {
  // Identity
  gameId: string;

  // Phase
  phase: "passing" | "playing" | "round_end" | "game_end";

  // Round context
  roundNumber: number;
  passDirection: "left" | "right" | "across" | null; // null = hold round

  // Player state (index = PlayerId)
  hands: Card[][]; // Each player's hand
  scores: number[]; // Cumulative scores
  roundScores: number[]; // Points taken this round

  // Current trick
  trick: Play[]; // Cards played so far (0-4)
  leadPlayer: PlayerId | null; // Who led this trick
  currentPlayer: PlayerId; // Whose turn

  // Derived (engine computes, renderer displays)
  validActions: PlayerAction[];
  heartsBroken: boolean;

  // Pass phase only
  pendingPasses?: {
    [key in PlayerId]?: Card[]; // Cards selected but not yet exchanged
  };
}
```

## PlayerAction (Renderer → Engine)

```typescript
type PlayerAction =
  | { type: "select_pass"; cards: [Card, Card, Card] }
  | { type: "play_card"; card: Card };
```

## Response

```typescript
interface ActionResult {
  ok: boolean;
  error?: string; // If !ok, why
  newState?: GameState; // If ok, updated state
}
```

## Design Notes

### What's in GameState

- **All derived state**: `validActions`, `heartsBroken` — renderer never
  computes
- **Full hands**: For pass-the-controller mode, all hands visible
- **Round and cumulative scores**: Both needed for display

### What's NOT in GameState

- Animation state (card positions, transitions)
- UI state (selected cards, hover)
- Player names/avatars (separate identity system)

### Visibility Variants

For networked play, server sends filtered GameState:

- Own hand: full cards
- Other hands: card count only
- This is a server concern, not interface change

## CLI Example

```
Round 1 | Pass: left | Hearts: not broken
Scores: [0, 0, 0, 0]

Trick: 3♣ 7♣ __  __
Lead: Player 0 | Current: Player 2

Your hand: 2♣ 5♦ 8♦ Q♦ 3♥ 7♥ J♥ 2♠ 5♠ 9♠ K♠

Valid: play 2♣
>
```

## Renderer Conventions (Preact)

Keep components as pure functions of (props) → JSX. This enables:

- Easy testing (render with mock state)
- Future portability (Preact → React is trivial)
- Clear data flow (state down, actions up)

```tsx
// Good: pure function of props
function Hand({ cards, onPlay }: { cards: Card[]; onPlay: (c: Card) => void }) {
  return (
    <div class="hand">
      {cards.map((card) => (
        <Card card={card} onClick={() => onPlay(card)} />
      ))}
    </div>
  );
}

// State lives at top level, passed down
function Game({
  state,
  dispatch,
}: {
  state: GameState;
  dispatch: (a: PlayerAction) => void;
}) {
  return (
    <div class="game">
      <Scores scores={state.scores} />
      <Trick trick={state.trick} />
      <Hand
        cards={state.hands[state.currentPlayer]}
        onPlay={(card) => dispatch({ type: "play_card", card })}
      />
    </div>
  );
}
```

**Rules:**

1. Components are pure functions of props
2. No `getElementById` or direct DOM queries
3. State in one place, passed down via props
4. Actions bubble up via callbacks
5. CSS classes for styling (stylesheet ports unchanged)
