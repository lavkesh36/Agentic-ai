from agent import Agent


def main() -> None:
    agent = Agent("Learner")
    agent.set_goal("Build a basic agentic AI model")

    initial_state = {
        "status": "idle",
        "progress": "start",
    }

    final_state = agent.run(initial_state, max_steps=4)

    print("Final state:", final_state)
    print("\nAgent history:")
    for entry in agent.history:
        print("-", entry)


if __name__ == "__main__":
    main()
