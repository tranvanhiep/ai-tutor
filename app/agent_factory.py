from crewai import LLM, Agent


class AgentFactory:
    """Factory to create agents dynamically."""

    @staticmethod
    def create_agent(
        role: str,
        goal: str,
        backstory: str,
        llm: LLM,
        allow_delegation: bool = False,
    ):
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            allow_delegation=allow_delegation,
            verbose=True,
            llm=llm,
        )
