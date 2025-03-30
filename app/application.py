from crewai import Agent, Process, Task
from app.agent_factory import AgentFactory
from config.config import Config
from app.crew_manager import CrewManager
from app.task_builder import TaskBuilder
from enums.llm_type import LLMType


class Application:
    """Main application to execute the crew."""

    def __init__(self, llm_type: LLMType = LLMType.LOCAL):
        self.config = Config()
        self.llm = self._get_llm(llm_type)
        self.crew_manager = CrewManager()

    def _get_llm(self, llm_type: LLMType):
        """Get the appropriate LLM based on type."""
        match llm_type:
            case LLMType.OPENAI:
                return self.config.get_openai_llm()
            case LLMType.GOOGLE:
                return self.config.get_google_llm()
            case LLMType.LOCAL | _:  # Default to LOCAL for any unmatched case
                return self.config.get_local_llm()

    def setup(self, total_students: int = 10):  # Reduced number of students for clarity
        """Setup the agents and tasks."""
        problem_solving_tasks: list[Task] = []
        students: list[Agent] = []

        # Create student problem solvers
        for i in range(total_students):
            student = AgentFactory.create_agent(
                role=f"Mathematics Student {i+1}",
                goal="Solve the mathematics problem and explain your solution clearly",
                backstory=(
                    "You are a grade {grade} student who approaches problems methodically.\n"
                    "You will:\n"
                    "1. Read and understand the problem carefully\n"
                    "2. Show your complete solution step by step\n"
                    "3. Verify your answer makes sense\n"
                    "4. Present your solution clearly"
                ),
                llm=self.llm,
                max_rpm=self.config.get_max_rpm(),
            )

            # Create problem-solving task for each student
            solve_task = TaskBuilder.create_task(
                description=(
                    "Solve this mathematics problem:\n\n"
                    "{question}\n\n"
                    "Show your complete solution following this format:\n"
                    "1. First explain what you understand from the problem\n"
                    "2. Show your step-by-step solution with explanations\n"
                    "3. State your final answer clearly\n"
                    "4. Verify your answer makes sense"
                ),
                expected_output=(
                    "# Understanding\n"
                    "* What I know:\n"
                    "* What I need to find:\n\n"
                    "# Solution Steps\n"
                    "1. Step 1\n"
                    "   * Work: [show calculation]\n"
                    "   * Because: [explain why]\n"
                    "[continue steps...]\n\n"
                    "# Final Answer\n"
                    "* The answer is: [state clearly]\n"
                    "* This makes sense because: [verify]\n"
                ),
                agent=student,
                async_execution=True,
            )

            students.append(student)
            problem_solving_tasks.append(solve_task)

        # Create solution verifier
        verifier = AgentFactory.create_agent(
            role="Solution Verifier",
            goal="Check student solutions and identify the correct one",
            backstory=(
                "You are a mathematics expert who verifies student solutions.\n"
                "Your job is to:\n"
                "1. Review each student's solution\n"
                "2. Compare their answers with the correct answer\n"
                "3. Identify which solution (if any) is correct"
            ),
            llm=self.llm,
            max_rpm=self.config.get_max_rpm(),
        )

        # Create verification task
        verify_task = TaskBuilder.create_task(
            description=(
                "TASK: Check student solutions against the correct answer\n\n"
                "Original Problem: {question}\n"
                "Correct Answer: {answer}\n\n"
                "Check if any student found the correct answer by:\n"
                "1. Looking at their final answers\n"
                "2. Comparing with the correct answer\n"
                "3. Stating if anyone got it right"
            ),
            expected_output=(
                "# Verification Results\n"
                "* Number of solutions checked: [number]\n"
                "* Correct solutions found: [yes/no]\n\n"
                "# Analysis\n"
                "* Student answers reviewed:\n"
                "  - Student 1: [their answer and step-by-step solution]\n"
                "  - Student 2: [their answer and step-by-step solution]\n"
                "  [continue for all students]\n\n"
                "# Conclusion\n"
                "* Correct solution found: [yes/no]\n"
                "* If yes, which student(s): [list them]\n"
                "* If no, explain why no one got it right\n"
            ),
            agent=verifier,
            context=problem_solving_tasks,
        )

        # Add agents and tasks to crew manager
        self.crew_manager.add_agents(*students, verifier)
        self.crew_manager.add_tasks(
            *problem_solving_tasks,
            verify_task
        )

    def run(self, inputs: dict):
        """Execute the crew and return the result."""
        crew = self.crew_manager.build_crew(
            process=Process.sequential,
            memory=False,
            embedder=self.config.get_google_embedder(),
        )
        result = crew.kickoff(inputs=inputs)
        return result
