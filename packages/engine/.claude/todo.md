---
managed-by: Skill(llm-subtask)
cost-benefit-sweh:
  timebox:
    "@value": 1.5
    rationale: |
      Only Phase 6 Steps 6-7 of the Immutability Refactor remain
      (per todo.d/2025-12-17-002). Phases 1-5 done; module pattern
      established; types/passing/start/ending packages migrated.
      Remaining is mechanical application of the established pattern.
    confidence: tentative
  benefit-2w:
    "@value": 0.5
    rationale: |
      Completes a refactor that's already paying off (hashable states,
      cleaner reasoning). Within 2w, finishing steps 6-7 is realistic.
    confidence: tentative
  cost-of-delay-2w:
    "@value": 0.1
    rationale: |
      Negligible. Pattern is established, refactor is near-done.
      Engine feature-complete with 70 passing tests; downstream
      prototype work doesn't strictly depend on steps 6-7.
    confidence: tentative
---

# Engine TODO

- [ ] [Immutability Refactor](todo.d/2025-12-17-002-immutability-refactor.md)
- [x] [Refactor SOA → AOS with PlayerState](todo.d/2025-12-17-001-refactor-soa-to-aos-playerstate.md)
