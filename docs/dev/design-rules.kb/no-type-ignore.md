# No Type Ignore

Avoid `# type: ignore` comments. They hide real issues and erode type safety.

## Techniques

- **TypeGuard over cast** - TypeGuard validates at runtime AND narrows types.
  Cast just lies to the checker.

- **Pattern matching for fixed-size tuples** - Tuple slicing loses element
  types. Match on indices and construct explicitly to preserve them.

- **Explicit yields for iterator arity** - When stdlib returns
  `Iterator[tuple[T, ...]]` but you need `Iterator[tuple[T, T, T]]`, unpack and
  yield to teach the checker the exact arity.

- **Purpose-built helpers over generic + cast** - If a generic method returns
  the wrong type for your use case, add a typed helper that returns exactly what
  you need.

- **zip with typed constants over enumerate** - `enumerate` returns `int`. If
  you need a `Literal` or newtype, zip with a typed constant tuple.
