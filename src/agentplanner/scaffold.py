"""Scaffold module: generates project structure from a plan."""

from pathlib import Path


def generate_scaffold(plan: dict, execute: bool = False) -> list:
    """
    Generate scaffold from plan.

    Args:
        plan: The structured plan with artifacts list.
        execute: If True, create files on disk. If False, dry-run only.

    Returns:
        List of artifact paths.
    """
    artifacts = _plan_to_files(plan)

    if execute:
        _execute_scaffold(artifacts)
    else:
        print("Scaffold preview (dry run):")
        for path in artifacts:
            print(f"  [would create] {path}")

    return artifacts


def _plan_to_files(plan: dict) -> list:
    """Extract artifact paths from plan."""
    return plan.get("artifacts", [])


def _execute_scaffold(artifacts: list) -> None:
    """Create directories and files on disk with rollback on failure."""
    print("Executing scaffold:")
    created_paths = []

    try:
        for path in artifacts:
            if path.endswith("/"):
                created = _create_directory(path)
            else:
                created = _create_file(path)

            if created:
                created_paths.append(created)

    except Exception as e:
        print(f"\n[error] {e}")
        _rollback(created_paths)
        raise


def _create_directory(path: str) -> Path | None:
    """Create a directory if it doesn't exist. Returns path if created."""
    dir_path = Path(path)

    if dir_path.exists():
        print(f"  [skip] {path} (already exists)")
        return None

    dir_path.mkdir(parents=True, exist_ok=True)
    print(f"  [create dir] {path}")
    return dir_path


def _create_file(path: str) -> Path | None:
    """Create a file with a TODO comment if it doesn't exist. Returns path if created."""
    file_path = Path(path)

    if file_path.exists():
        print(f"  [skip] {path} (already exists)")
        return None

    # Create parent directories if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write minimal TODO content
    # TODO: Generate file contents based on task descriptions
    content = f"# TODO: Implement {file_path.name}\n"
    file_path.write_text(content)
    print(f"  [create file] {path}")
    return file_path


def _rollback(created_paths: list) -> None:
    """Delete paths created during this run. Files first, then directories."""
    if not created_paths:
        return

    print("\nRolling back:")

    # Separate files and directories
    files = [p for p in created_paths if p.is_file()]
    dirs = [p for p in created_paths if p.is_dir()]

    # Delete files first
    for file_path in files:
        try:
            file_path.unlink()
            print(f"  [rollback] deleted file: {file_path}")
        except Exception as e:
            print(f"  [rollback failed] {file_path}: {e}")

    # Delete directories in reverse order (deepest first)
    dirs.sort(key=lambda p: len(p.parts), reverse=True)
    for dir_path in dirs:
        try:
            dir_path.rmdir()
            print(f"  [rollback] deleted dir: {dir_path}")
        except Exception as e:
            print(f"  [rollback failed] {dir_path}: {e}")
