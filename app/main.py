from app.planner import create_plan
from app.critic import evaluate_plan
import json

MAX_ITERATIONS = 2
SCORE_THRESHOLD = 0.85

def main():
    query = "How to improve retention in a gaming app?"

    feedback = None
    plan = None

    for iteration in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {iteration + 1} ---")

        # Planner
        plan = create_plan(query, feedback)

        if not plan:
            print("Plan generation failed")
            return

        plan_dict = plan.model_dump()
        print("PLAN:")
        print(plan_dict)

        # Convert to clean JSON string
        plan_str = json.dumps(plan_dict, indent=2)

        # Critic
        critique = evaluate_plan(plan_str)

        if not critique:
            print("Critic failed")
            return

        critique_dict = critique.model_dump()
        print("\nCRITIC:")
        print(critique_dict)

        score = critique_dict["score"]
        issues = critique_dict["issues"]

        # ✅ STOPPING CONDITION
        if score >= SCORE_THRESHOLD and len(issues) <= 1:
            print("\n✅ Stopping condition met")
            break

        # Prepare feedback for next iteration
        feedback = "\n".join(issues + critique_dict["suggestions"])

    print("\n🎯 FINAL PLAN:")
    print(plan.model_dump())


if __name__ == "__main__":
    main()