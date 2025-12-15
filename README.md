# AgentPlanner

AgentPlanner is a simple, safety-focused CLI tool that turns natural language
feature requests into structured engineering plans.

The project explores how agent-style orchestration can be used for planning and
execution workflows, while keeping behavior deterministic and easy to reason about.

---

## What It Does

Given a short description of a software feature, AgentPlanner:

1. Generates a structured implementation plan
2. Validates the plan against a strict schema
3. Reviews the plan for basic quality issues
4. Refines the plan if needed
5. Previews a project scaffold (dry-run by default)

The tool never executes changes unless explicitly requested.

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
      "title": "Core Implementation",
      "tasks": [
        {
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
    "README.md"
  ],
  "status": "draft"
}
Dry-Run Scaffold Preview
text
Copy code
Scaffold preview (dry run):
  [would create] src/
  [would create] src/core.py
  [would create] README.md
No files are written unless execution is explicitly enabled.

Architecture (High Level)
csharp
Copy code
cli.py         - Orchestrates the workflow
planner.py    - Generates plans
validation.py - Enforces schema correctness
reviewer.py   - Checks plan quality
refiner.py    - Improves rejected plans
scaffold.py   - Previews or executes file creation
Each step is isolated and designed to fail safely.

LLM Integration
LLM integration is not enabled yet.

Plan generation is currently deterministic and simulated. This is intentional,
so that orchestration, validation, and execution logic can be developed and tested
without relying on external APIs.

LLM support is planned as a future improvement and will reuse the same safety gates.

Project Status
This project is experimental and focuses on learning:

agent-style orchestration

safe execution patterns

structured planning workflows