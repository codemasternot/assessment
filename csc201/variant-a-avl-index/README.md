# Variant A — AVL-backed Mutable Index

You are maintaining a small in-memory index used by a service that stores records under integer keys. The index supports insert/update, lookup, deletion, sorted iteration, and inclusive range queries.

The implementation is expected to maintain the standard AVL/BST invariants after **every** mutation.

## Your task

During the live assessment you must:

1. orient yourself in the repository and state the important representation invariants;
2. discover and reproduce a correctness/invariant defect with a small operation sequence;
3. repair the root cause and add regression tests;
4. identify an avoidable performance problem in an assessed workload and improve it without changing the public API;
5. run the benchmark harness before and after the optimisation;
6. complete the AI review phase only after phases 1–4 are finished;
7. submit the work as a GitHub Pull Request using the requirements in `../ASSESSMENT_4_RULES.md`.

## Public API

`AVLIndex` supports:

- `set(key, value)`
- `get(key, default=None)`
- `delete(key)`
- `items()`
- `range_items(low, high)`
- `validate()`
- `height()`

Do not replace the implementation with a third-party balanced-tree package.

## Required evidence

Your PR must include:

- the smallest failing sequence you found;
- the exact invariant/correctness condition that fails;
- a regression test for that sequence or a smaller equivalent;
- an explanation of the repair;
- complexity before/after for the performance change;
- benchmark evidence using `benchmark.py` or an assessor-approved equivalent.

## Local commands

```bash
python -m pytest -q
python benchmark.py
```

Visible tests are not exhaustive. Passing them does not establish full correctness.
