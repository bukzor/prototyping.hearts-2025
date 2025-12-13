# Testing

| Python | Rust |
|--------|------|
| pytest | cargo test |
| hypothesis | proptest |

## Notes

- proptest is the direct hypothesis analog (shrinking, strategy composition)
- quickcheck exists but proptest is closer to hypothesis in spirit
- Both support property-based testing for game logic validation
