"""Validation module: validates plan schema before execution."""

REQUIRED_KEYS = ["feature", "milestones", "artifacts", "status"]
VALID_PRIORITIES = ["high", "medium", "low"]


def validate_plan(plan: dict) -> None:
    """
    Validate plan structure and raise ValueError if invalid.

    Args:
        plan: The plan dict to validate.

    Raises:
        ValueError: If plan does not match expected schema.
    """
    _validate_top_level(plan)
    _validate_milestones(plan["milestones"])
    _validate_artifacts(plan["artifacts"])


def _validate_top_level(plan: dict) -> None:
    """Validate plan is a dict with required keys."""
    if not isinstance(plan, dict):
        raise ValueError("Plan must be a dict")

    for key in REQUIRED_KEYS:
        if key not in plan:
            raise ValueError(f"Missing required key: '{key}'")


def _validate_milestones(milestones) -> None:
    """Validate milestones list and each milestone."""
    if not isinstance(milestones, list):
        raise ValueError("'milestones' must be a list")

    if len(milestones) == 0:
        raise ValueError("'milestones' must not be empty")

    for i, milestone in enumerate(milestones):
        _validate_milestone(milestone, i)


def _validate_milestone(milestone: dict, index: int) -> None:
    """Validate a single milestone."""
    prefix = f"milestones[{index}]"

    if not isinstance(milestone, dict):
        raise ValueError(f"{prefix} must be a dict")

    if "id" not in milestone:
        raise ValueError(f"{prefix} missing 'id'")
    if not isinstance(milestone["id"], int):
        raise ValueError(f"{prefix}.id must be an int")

    if "title" not in milestone:
        raise ValueError(f"{prefix} missing 'title'")
    if not isinstance(milestone["title"], str):
        raise ValueError(f"{prefix}.title must be a str")

    if "tasks" not in milestone:
        raise ValueError(f"{prefix} missing 'tasks'")

    _validate_tasks(milestone["tasks"], prefix)


def _validate_tasks(tasks, prefix: str) -> None:
    """Validate tasks list and each task."""
    if not isinstance(tasks, list):
        raise ValueError(f"{prefix}.tasks must be a list")

    if len(tasks) == 0:
        raise ValueError(f"{prefix}.tasks must not be empty")

    for i, task in enumerate(tasks):
        _validate_task(task, f"{prefix}.tasks[{i}]")


def _validate_task(task: dict, prefix: str) -> None:
    """Validate a single task."""
    if not isinstance(task, dict):
        raise ValueError(f"{prefix} must be a dict")

    required_fields = [
        ("step", int),
        ("description", str),
        ("output", str),
        ("priority", str),
    ]

    for field, expected_type in required_fields:
        if field not in task:
            raise ValueError(f"{prefix} missing '{field}'")
        if not isinstance(task[field], expected_type):
            raise ValueError(f"{prefix}.{field} must be a {expected_type.__name__}")

    if task["priority"] not in VALID_PRIORITIES:
        raise ValueError(
            f"{prefix}.priority must be one of {VALID_PRIORITIES}, got '{task['priority']}'"
        )


def _validate_artifacts(artifacts) -> None:
    """Validate artifacts list."""
    if not isinstance(artifacts, list):
        raise ValueError("'artifacts' must be a list")

    if len(artifacts) == 0:
        raise ValueError("'artifacts' must not be empty")

    for i, artifact in enumerate(artifacts):
        if not isinstance(artifact, str):
            raise ValueError(f"artifacts[{i}] must be a str")
