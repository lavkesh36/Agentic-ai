from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Action:
    name: str
    description: str


class Agent:
    """A simple agentic AI model for learning and experimentation."""

    def __init__(self, name: str):
        self.name = name
        self.goal = ""
        self.memory: List[str] = []
        self.history: List[str] = []

    def set_goal(self, goal: str) -> None:
        self.goal = goal.strip()
        self.memory.append(f"Goal set: {self.goal}")
        self.history.append(f"Agent received goal: {self.goal}")

    def perceive(self, state: Dict[str, str]) -> Dict[str, str]:
        observation = {
            "status": state.get("status", "unknown"),
            "progress": state.get("progress", "none"),
        }
        self.memory.append(f"Perceived state: {observation}")
        return observation

    def plan(self, observation: Dict[str, str]) -> List[Action]:
        steps: List[Action] = []

        if not self.goal:
            return [Action("No goal", "There is nothing to plan without a goal.")]

        if "write" in self.goal.lower() or "build" in self.goal.lower():
            steps = [
                Action("Define", "Clarify what the model should do."),
                Action("Research", "Gather the required steps and examples."),
                Action("Implement", "Write the first version of the model."),
                Action("Review", "Check the result and improve it."),
            ]
        elif "plan" in self.goal.lower() or "organize" in self.goal.lower():
            steps = [
                Action("Collect", "Collect the main objectives."),
                Action("Sequence", "Order tasks by priority."),
                Action("Assign", "Assign tasks and set deadlines."),
                Action("Check", "Confirm the plan is complete."),
            ]
        else:
            steps = [
                Action("Interpret", "Understand the goal requirements."),
                Action("Outline", "Create a basic plan for the goal."),
                Action("Execute", "Take the first action toward the goal."),
                Action("Reflect", "Review what happened and adjust."),
            ]

        self.memory.append(f"Created plan with {len(steps)} steps.")
        return steps

    def act(self, action: Action, state: Dict[str, str]) -> Dict[str, str]:
        result_message = f"Executing action: {action.name} - {action.description}"
        self.history.append(result_message)
        state["status"] = f"{action.name} completed"
        state.setdefault("progress", "")
        state["progress"] += f"{action.name} -> "
        self.memory.append(result_message)
        return state

    def reflect(self) -> None:
        reflection = f"Reflecting after goal '{self.goal}' with {len(self.memory)} memory entries."
        self.memory.append(reflection)
        self.history.append(reflection)

    def run(self, state: Dict[str, str], max_steps: int = 5) -> Dict[str, str]:
        observation = self.perceive(state)
        plan = self.plan(observation)

        step_count = 0
        for action in plan:
            if step_count >= max_steps:
                break
            if action.name == "No goal":
                self.history.append("No goal was set, stopping.")
                break
            state = self.act(action, state)
            step_count += 1

        self.reflect()
        return state
