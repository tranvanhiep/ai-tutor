from crewai import Agent, Task


class TaskBuilder():
    """Builder for creating tasks with dependencies."""

    @staticmethod
    def create_task(description: str, expected_output: str, agent: Agent):
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
        )
