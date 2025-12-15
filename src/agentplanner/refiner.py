"""Refiner module: improves plan based on review feedback."""

import copy
import re


def refine_plan(plan: dict, review: dict) -> dict:
    """
    Refine plan based on review feedback.

    Args:
        plan: The original plan dict.
        review: The review dict with issues and suggestions.

    Returns:
        A new refined plan dict (original is not modified).
    """
    refined = copy.deepcopy(plan)

    # Fix issues
    _fix_missing_artifacts(refined, review.get("issues", []))
    _fix_vague_descriptions(refined, review.get("issues", []))

    # Apply suggestions
    _apply_suggestions(refined, review.get("suggestions", []))

    return refined


def _fix_missing_artifacts(plan: dict, issues: list) -> None:
    """Add missing artifacts mentioned in issues."""
    artifacts = plan.get("artifacts", [])
    artifacts_set = set(artifacts)

    for issue in issues:
        # Look for pattern: "Task output 'X' not in artifacts list"
        match = re.search(r"output '([^']+)' not in artifacts", issue)
        if match:
            missing_artifact = match.group(1)
            if missing_artifact not in artifacts_set:
                artifacts.append(missing_artifact)
                artifacts_set.add(missing_artifact)

    plan["artifacts"] = artifacts


def _fix_vague_descriptions(plan: dict, issues: list) -> None:
    """Clarify vague task descriptions."""
    vague_tasks = set()

    for issue in issues:
        # Look for pattern: "Task 'X' has vague description"
        match = re.search(r"Task '([^']+)' has vague description", issue)
        if match:
            vague_tasks.add(match.group(1))

    # Update matching tasks
    for milestone in plan.get("milestones", []):
        for task in milestone.get("tasks", []):
            desc = task.get("description", "")
            if desc in vague_tasks:
                task["description"] = f"{desc} (clarified during refinement)"


def _apply_suggestions(plan: dict, suggestions: list) -> None:
    """Apply suggestions to improve the plan."""
    artifacts = plan.get("artifacts", [])
    artifacts_set = set(artifacts)

    for suggestion in suggestions:
        suggestion_lower = suggestion.lower()

        # Add test file if suggested
        if "test" in suggestion_lower:
            test_file = "tests/test_basic.py"
            if test_file not in artifacts_set:
                artifacts.append(test_file)
                artifacts_set.add(test_file)
                # Also add tests directory
                if "tests/" not in artifacts_set:
                    artifacts.append("tests/")
                    artifacts_set.add("tests/")

        # Add README if suggested
        if "readme" in suggestion_lower or "documentation" in suggestion_lower:
            readme = "README.md"
            if readme not in artifacts_set:
                artifacts.append(readme)
                artifacts_set.add(readme)

    plan["artifacts"] = artifacts
