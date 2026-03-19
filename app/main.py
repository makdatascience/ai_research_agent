from app.planner import create_plan

def main():
    query = "How to improve user retention in a gaming app?"
    plan = create_plan(query)
    print(plan)

if __name__ == "__main__":
    main()