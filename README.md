# AIAIU CSC-201 Live DSA Assessment Bank

This repository contains practical assessment variants for **CSC-201: Data Structures & Algorithms**.

The main focus is the course's live Assessment 4: **Live DSA Repair, Optimisation & Pull Request**. Each variant gives the student an unfamiliar Python repository containing a real correctness/invariant defect and a separate avoidable performance problem.

## Student conditions

- 100 minutes total.
- Phases 1–4 are human-only: repository orientation, defect reproduction, repair/regression testing, and performance diagnosis/optimisation.
- AI may be used only during the dedicated review phase after the student's own repair and optimisation are complete.
- The final state must be a reviewable GitHub branch and Pull Request with evidence.
- Students are assessed on reasoning, invariants, tests, complexity, measured evidence, and their ability to defend the change—not merely on getting the tests green.

## Assessment variants

- `csc201/variant-a-avl-index/` — mutable AVL-backed index with a deletion/rebalancing defect and a query hot path.
- `csc201/variant-b-hash-cache/` — open-addressed hash table/cache with a deletion/probing defect and avoidable eviction cost.
- `csc201/variant-c-graph-router/` — weighted graph router with a state/correctness defect and repeated shortest-path performance problem.

Each folder contains a student brief, starter implementation, visible tests, and a local benchmark/profiling harness. **No solution keys are stored in this public repository.** Assessors should maintain hidden tests and marking notes separately.
