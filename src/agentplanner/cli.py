"""CLI entry point for AgentPlanner."""

import argparse
import json
from agentplanner import planner, scaffold
from agentplanner.validation import validate_plan
from agentplanner.reviewer import review_plan
from agentplanner.refiner import refine_plan


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="AgentPlanner CLI")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview scaffold without creating files (default behavior)",
    )
    group.add_argument(
        "--execute",
        action="store_true",
        help="Execute scaffold generation",
    )
    return parser.parse_args()



def main():
    """Main entry point: orchestrate planning and scaffolding."""
    args = parse_args()

    # Step 1: Read feature request
    feature_request = input("Enter your feature request: ")
    if not feature_request.strip():
        print("Error: Empty feature request.")
        return

    # Step 2: Generate plan
    try:
        plan = planner.generate_plan(feature_request)
        validate_plan(plan)
    except ValueError as e:
        print(f"Plan validation failed: {e}")
        return
    
    MAX_REFINEMENTS = 2
    attempt = 0

    while True:
        review = review_plan(plan)

        if review["approved"]:
            break

        if attempt >= MAX_REFINEMENTS:
            print("\nPlan review failed after refinements:")
            for issue in review["issues"]:
                print(f"- {issue}")
            return

        print("\nPlan not approved, refining...")
        plan = refine_plan(plan, review)
        attempt += 1
        

    print("\nGenerated Plan:")
    print(json.dumps(plan, indent=2))

    # Step 3: Scaffold generation
    print()
    if args.execute:
        scaffold.generate_scaffold(plan, execute=True)
    else:
        scaffold.generate_scaffold(plan)


if __name__ == "__main__":
    main()
