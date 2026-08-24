# Variant C — Weighted Graph Router

You are maintaining a mutable weighted **undirected** graph used to answer shortest-route queries. Vertices are hashable IDs and edge weights are non-negative numbers.

The router must return an actual path and its total cost, preserve undirected-edge symmetry under mutation, and remain correct when there are multiple competing routes to a vertex.

## Your task

1. State the graph and shortest-path correctness conditions that matter.
2. Discover a small graph/query that demonstrates a correctness defect.
3. Repair the root cause and add regression tests.
4. Diagnose an avoidable performance problem in a repeated-query workload and improve it without returning stale answers after graph mutation.
5. Produce before/after benchmark evidence.
6. Use AI only in the dedicated review phase after phases 1–4.
7. Submit the work as a GitHub Pull Request under `../ASSESSMENT_4_RULES.md`.

## Public API

`GraphRouter` supports:

- `add_edge(a, b, weight)`
- `remove_edge(a, b)`
- `shortest_path(source, target)` → `(cost, path)` or `(inf, [])`
- `neighbors(node)`
- `validate()`

Negative edge weights are invalid. Do not replace the implementation with NetworkX or another graph library.

## Required evidence

Your PR must contain the smallest failing graph/query you found, the precise correctness condition, regression tests, repair rationale, complexity before/after, and benchmark/profiling evidence.

```bash
python -m pytest -q
python benchmark.py
```

Visible tests are not exhaustive.
