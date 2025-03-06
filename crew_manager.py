from typing import List
from crewai import Agent, Crew, Process, Task


class CrewManager:
    """Manages crew of agents and tasks."""

    def __init__(self):
        self.agents: List[Agent] = []
        self.tasks: List[Task] = []

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def add_agents(self, *agents: Agent):
        self.agents.extend(agents)

    def add_tasks(self, *tasks: Task):
        self.tasks.extend(tasks)

    def build_crew(self, process: Process, memory: bool, embedder: dict | None):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=process,
            memory=memory,
            embedder=embedder,
        )
