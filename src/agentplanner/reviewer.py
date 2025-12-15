"""Reviewer module: reviews plan quality before execution."""

VAGUE_WORDS = ["something", "stuff", "things", "etc", "various", "misc"]


def review_plan(plan: dict) -> dict:
    """
    Review plan quality and return feedback.

    Args:
        plan: The plan dict to review.

    Returns:
        dict with: approved (bool), issues (list), suggestions (list)
    """
    issues = []
    suggestions = []

    # Check artifacts
    issues.extend(_check_artifacts(plan))

    # Check task outputs match artifacts
    issues.extend(_check_outputs_in_artifacts(plan))

    # Check for vague content
    issues.extend(_check_vague_content(plan))

    # Generate suggestions
    suggestions.extend(_generate_suggestions(plan))

    approved = len(issues) == 0

    return {
        "approved": approved,
        "issues": issues,
        "suggestions": suggestions,
    }


def _check_artifacts(plan: dict) -> list:
    """Check if artifacts list is valid."""
    issues = []
    artifacts = plan.get("artifacts", [])

    if len(artifacts) == 0:
        issues.append("Artifacts list is empty")

    return issues


def _check_outputs_in_artifacts(plan: dict) -> list:
    """Check if task outputs are represented in artifacts."""
    issues = []
    artifacts = set(plan.get("artifacts", []))
    milestones = plan.get("milestones", [])

    for milestone in milestones:
        for task in milestone.get("tasks", []):
            output = task.get("output", "")
            if output and output not in artifacts:
                issues.append(f"Task output '{output}' not in artifacts list")

    return issues


def _check_vague_content(plan: dict) -> list:
    """Check for vague milestone titles or task descriptions."""
    issues = []
    milestones = plan.get("milestones", [])

    for milestone in milestones:
        title = milestone.get("title", "").lower()
        if _is_vague(title):
            issues.append(f"Milestone '{milestone.get('title')}' has vague title")

        for task in milestone.get("tasks", []):
            desc = task.get("description", "").lower()
            if _is_vague(desc):
                issues.append(f"Task '{task.get('description')}' has vague description")

    return issues


def _is_vague(text: str) -> bool:
    """Check if text contains vague words."""
    for word in VAGUE_WORDS:
        if word in text:
            return True
    return False


def _generate_suggestions(plan: dict) -> list:
    """Generate improvement suggestions."""
    suggestions = []
    milestones = plan.get("milestones", [])

    # Suggest adding tests if none mentioned
    has_test_artifact = any("test" in a.lower() for a in plan.get("artifacts", []))
    if not has_test_artifact:
        suggestions.append("Consider adding test files to artifacts")

    # Suggest documentation if missing
    has_docs = any(a.endswith(".md") for a in plan.get("artifacts", []))
    if not has_docs:
        suggestions.append("Consider adding documentation (README.md)")

    # Suggest more milestones if only one
    if len(milestones) == 1:
        suggestions.append("Consider breaking work into multiple milestones")

    return suggestions
