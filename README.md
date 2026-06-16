# ARC-AGI Task Solver

A Python-based solver for ARC-AGI style reasoning tasks that automatically identifies the underlying task type and generates the correct output using symbolic reasoning and grid transformations.

## Overview

The Abstract Reasoning Corpus (ARC-AGI) is a benchmark designed to evaluate abstraction, reasoning, and generalization capabilities.

This project was developed as part of the AI Club (CFI IIT Madras) Viveka challenge, where the objective was to:

1. Identify which of two ARC-style tasks an input grid belongs to.
2. Apply the appropriate reasoning procedure.
3. Generate the correct output grid.

Unlike machine learning approaches, this solution uses interpretable rule-based reasoning and object-centric analysis.

---

## Features

### Automatic Task Identification

The solver first determines whether the input belongs to:

* Problem Type 1
* Problem Type 2

and routes execution to the appropriate solution pipeline.

### Problem 1

Uses:

* Grid partitioning
* Object extraction
* Pattern masking
* Domino counting
* Shape replication

### Problem 2

Uses:

* Boundary detection
* Connected component analysis
* Object merging
* Bounding-box extraction
* Geometric reconstruction

---

## Approach

```text
Input Grid
      │
      ▼
Task Classification
      │
 ┌────┴────┐
 ▼         ▼
Problem1  Problem2
Solver    Solver
 └────┬────┘
      ▼
Output Grid
```

---

## Key Techniques

* Connected Component Analysis
* Object Detection
* Pattern Extraction
* Grid Reasoning
* Rule-Based Transformations
* Spatial Reasoning

---

## Running the Solver

```bash
python solver.py
```

Input should follow ARC JSON format.

Example:

```json
[
  [0,0,1],
  [1,1,0]
]
```

The generated solution is written to:

```text
output.json
```

---

## Repository Structure

```text
arc-agi-task-solver/
│
├── README.md
├── solver.py
├── test_cases/
```

---

## Motivation

ARC tasks are designed to test abstraction and fluid intelligence rather than memorization.

This project demonstrates how symbolic reasoning and explicit rule extraction can solve structured reasoning tasks without training a neural network.

---

## Technologies

* Python
* JSON
* Graph Traversal (DFS)
* Connected Components
* Grid Manipulation

---

## Future Improvements

* Generalized ARC task framework
* Automatic rule discovery
* Support for additional ARC task families
* Hybrid symbolic + neural approaches
