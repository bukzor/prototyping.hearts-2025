# Testing

Test runners and property-based testing.

| | POC | Production |
|-|-----|------------|
| Test runner | pytest | cargo test |
| Property testing | hypothesis | proptest |

## Notes

- proptest is the direct hypothesis analog (shrinking, strategy composition)
- quickcheck exists but proptest is closer to hypothesis in spirit
- Both support property-based testing for game logic validation
