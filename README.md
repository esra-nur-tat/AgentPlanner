# AgentPlanner

AgentPlanner is a small, safety-focused CLI tool that turns natural language
feature requests into structured, engineering-ready implementation plans.

The project explores how **agent-style orchestration** can be used for planning
and execution workflows while keeping behavior deterministic, inspectable,
and easy to reason about.

---

## What It Does

Given a short description of a software feature, AgentPlanner:

1. Generates a structured implementation plan
2. Validates the plan against a strict schema (hard gate)
3. Reviews the plan for basic quality issues (soft gate)
4. Refines the plan if needed
5. Previews a project scaffold (dry-run by default)

No files are written to disk unless execution is explicitly enabled.

---

## Example Demo Run

### Input

```text
Create a CLI tool that orchestrates planning, review, and execution steps for software projects
Output (Plan)
json
Copy code
{
  "feature": "Create a CLI tool that orchestrates planning, review, and execution steps for software projects",
  "milestones": [
    {
      "id": 1,
      "title": "Core Implementation",
      "tasks": [
        {
          "step": 1,
          "description": "Analyze requirements",
          "output": "requirements.md",
          "priority": "high"
        },
        {
          "step": 2,
          "description": "Implement core logic",
          "output": "src/core.py",
          "priority": "high"
        }
      ]
    }
  ],
  "artifacts": [
    "src/",
    "src/core.py",
    "README.md",
    "requirements.md"
  ],
  "status": "draft"
}
## Dry-Run Scaffold Preview
text
Copy code
Scaffold preview (dry run):
  [would create] src/
  [would create] src/core.py
  [would create] README.md
  [would create] requirements.md
By default, this is a preview only. Execution must be explicitly requested.

## Architecture (High Level)
csharp
Copy code
cli.py         - Orchestrates the workflow
planner.py    - Generates structured plans
validation.py - Enforces schema correctness
reviewer.py   - Checks plan quality
refiner.py    - Improves rejected plans
scaffold.py   - Previews or executes file creation
Each step has a single responsibility, and side effects are isolated.

##Design Principles
Safety First

Dry-run by default

Explicit execution

Rollback on failure

Determinism

Same input produces the same output

No hidden randomness

No automatic decision-making

Separation of Concerns

Planning, validation, review, refinement, and execution are independent stages

## LLM Integration Status
LLM integration is not enabled yet.

Plan generation is currently deterministic and simulated. This is intentional,
so that orchestration, validation, and execution logic can be developed and
tested without relying on external APIs.

## TODO (Future Work)
Replace the simulated planner with an LLM-backed planner

Enable semantic task decomposition

Keep the same validation, review, and execution safety gates

## Project Status
This project is experimental and learning-focused.
The current goal is to build a clear, safe, and extensible orchestration pipeline
rather than a production-ready automation system.
