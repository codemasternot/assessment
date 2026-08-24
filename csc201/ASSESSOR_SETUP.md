# CSC-201 Assessor Setup Guide

The repository is public, so **do not commit solution keys, minimal failing sequences, hidden tests, or expected optimisation patches here**.

## Recommended delivery workflow

1. Select one variant for a student.
2. Record the baseline commit SHA before the session.
3. Give the student the selected folder and the common `ASSESSMENT_4_RULES.md`.
4. Require a dedicated branch such as `assessment/csc201-variant-a-<student-id>`.
5. Start the 100-minute clock only after the environment and visible tests run successfully.
6. Enforce the human-only rule for phases 1–4.
7. At the start of phase 5, explicitly permit AI use and require the student to record material suggestions in the PR template.
8. Before time expires, require a pushed branch and Pull Request.
9. Run private/hidden tests against the PR head SHA.
10. Conduct the oral defence from the actual PR diff and evidence.

## Hidden-test design

For every variant maintain private tests that cover:

- at least one short counterexample exposing the intended correctness defect;
- neighbouring cases that defeat symptom-only patches;
- randomized/adversarial operation sequences where appropriate;
- public API compatibility;
- mutation after optimisation so stale caches/indexes are detected;
- one scale/performance check with a generous but meaningful bound.

Hidden tests should test **properties**, not one exact implementation. A different correct repair must be able to pass.

## Evidence to preserve

Record:

- baseline commit SHA;
- student branch and PR number;
- assessment start/end time;
- visible and hidden test results;
- before/after benchmark evidence;
- oral questions asked and summary of answers;
- live PASS / NOT YET decision and reasons.

## Academic-integrity note

The first four phases are intended to establish independent foundational DSA competence. AI is deliberately introduced later to test professional verification and judgement rather than banning modern development tools entirely.
