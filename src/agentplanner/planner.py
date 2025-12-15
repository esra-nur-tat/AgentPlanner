"""Planner module: converts feature requests into structured plans."""


def generate_plan(feature_request: str) -> dict:
    """
    Convert a feature request into a structured implementation plan.

    Args:
        feature_request: Natural language description of the feature.

    Returns:
        A dict representing the structured plan.
    """
    prompt = _build_prompt(feature_request)
    plan_data = _call_llm(prompt)

    plan = {
        "feature": feature_request,
        "milestones": plan_data["milestones"],
        "artifacts": plan_data["artifacts"],
        "status": "draft",
    }

    return plan


def _build_prompt(feature_request: str) -> str:
    """Build prompt for the LLM."""
    # TODO: Improve prompt with schema definition and examples
    # TODO: Add output format instructions for milestones/tasks/artifacts
    return f"Create an implementation plan for: {feature_request}"


def _call_llm(prompt: str) -> dict:
    """
    Simulate an LLM call that returns a structured plan.

    TODO: Replace with real LLM call:
        - Use Claude API (anthropic library) or OpenAI API
        - Parse JSON response from LLM
        - Validate response matches schema
        - Handle API errors and retries
    """
    # Simulated response - ignores prompt for now
    return {
        "milestones": [
            {
                "id": 1,
                "title": "Core Implementation",
                "tasks": [
                    {"step": 1, "description": "Analyze requirements", "output": "requirements.md", "priority": "high"},
                    {"step": 2, "description": "Implement core logic", "output": "src/core.py", "priority": "high"},
                ],
                
            },
            {
                "id": 2,
                "title": "Testing and Documentation",
                "tasks": [
                    {"step": 1, "description": "Write unit tests", "output": "tests/test_core.py", "priority": "medium"},
                    {"step": 2, "description": "Add documentation", "output": "README.md", "priority": "low"},
                ],
            },
        ],
        "artifacts": [
            "src/",
            "src/core.py",
            "tests/",
            "tests/test_core.py",
            "README.md",
        ],
    }
