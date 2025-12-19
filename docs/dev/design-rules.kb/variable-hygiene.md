# Variable Hygiene

Reduce noise from unnecessary intermediate names.

## Inline Single-Use Variables

If a variable is used exactly once, inline it—unless the name adds significant
clarity.

```python
# Avoid
new_hand = Hand(hand - {card})
new_players = update_player(state.players, player, hand=new_hand)

# Prefer
new_players = update_player(
    state.players, player, hand=Hand(hand - {card})
)
```

## Rebind Evolving Values In-Place

When a value transforms through stages, use the same name:

```python
# Good
state = replace(state, players=new_players)
state = check_game_end(state)
return state

# Avoid
new_state = replace(state, players=new_players)
final_state = check_game_end(new_state)
return final_state
```

## Keep Names That Document Intent

Some single-use names are worth keeping:

- `winner` — documents what the value means
- `shooter` — domain term
- `direction` — clarifies a complex expression

Use judgment: if removing the name hurts readability, keep it.

## Tooling

Run `/polish-vars` after completing a feature to apply these rules.
