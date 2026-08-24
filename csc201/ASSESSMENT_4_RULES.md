# CSC-201 Assessment 4 — Live DSA Repair, Optimisation & Pull Request

**Weight:** 20 marks  
**Time:** 100 minutes  
**Pass requirement:** 15/20 **and** mandatory live PASS

## What the student receives

The assessor assigns exactly one assessment variant. The repository contains a small unfamiliar algorithmic system, visible tests, and a benchmark/profiling harness. The supplied implementation contains:

1. at least one **correctness/invariant defect**; and
2. at least one **avoidable performance/complexity problem**.

The student is not told the exact defect location.

## Timed phases

| Phase | Time | Required performance |
|---|---:|---|
| 1. Repository orientation | 10 min | Identify the ADTs, invariants, hot path, tests, and likely risk areas. |
| 2. Reproduce invariant defect | 15 min | Produce a small failing sequence/input and state the exact broken invariant or correctness condition. |
| 3. Repair + regression tests | 20 min | Fix the root cause and add tests that fail on the original code and pass on the repair. |
| 4. Performance diagnosis | 20 min | Identify an avoidable complexity/performance problem, implement a justified improvement, and measure it. |
| 5. AI review phase | 15 min | AI may critique the solution. Verify each material suggestion; accept or reject with reasons. |
| 6. GitHub PR + defence | 20 min | Commit, push, open a Pull Request, and defend the correctness/performance evidence. |

**Human-only:** phases 1–4. Local Python documentation and assessor-supplied references may be used. AI/LLM/code-agent use begins only in phase 5.

## Required final repository state

Before time expires, the student must have:

- a dedicated challenge branch created from the supplied baseline;
- at least one meaningful commit for the correctness repair;
- at least one meaningful commit for the performance change, unless the assessor approves another split;
- new regression tests committed to the branch;
- benchmark/profiling evidence committed in a compact reproducible form;
- a Pull Request whose description contains:
  - root cause;
  - broken invariant/correctness condition;
  - repair rationale;
  - complexity before/after;
  - test and benchmark evidence;
  - remaining limitations;
  - AI-review decisions from phase 5.

## Marking — 20 marks

| Competency | Marks | High-level evidence |
|---|---:|---|
| Invariant/correctness diagnosis | 4 | Small failing sequence, root cause, exact broken condition. |
| Correct repair + regression tests | 4 | Repair addresses root cause and tests would catch recurrence. |
| Algorithm/performance improvement | 5 | Improvement is justified by complexity analysis and measured evidence. |
| AI critique + technical judgement | 3 | Suggestions are verified rather than accepted automatically. |
| GitHub PR + oral defence | 4 | Clear diff, rationale, tests, complexity/invariant impact, reproducible evidence. |

A wrong first hypothesis is acceptable if the student tests it, updates from evidence, and recovers. Random edits, unsupported complexity claims, or unexplained AI-generated patches are heavily penalised.

## Mandatory live PASS / NOT YET gate

Automatic **NOT YET** if the student cannot explain their submitted repair, cannot reconstruct a key reasoning step, silently breaks a stated invariant, cannot trace benchmark evidence to the branch/PR, or cannot distinguish the AI's suggestion from their own verified engineering judgement.

## Assessor oral prompts

The assessor should select at least three:

- What is the smallest input or operation sequence that breaks the original implementation?
- State the invariant/correctness condition in one sentence.
- Why does your repair restore it for all relevant cases rather than only this example?
- What is the dominant operation before and after your optimisation?
- What input distribution would make your optimisation less useful or worse?
- Show the exact regression test that proves the old defect.
- Show the benchmark/profiling evidence and explain what it does **not** prove.
- Which AI suggestion did you reject or modify, and why?
