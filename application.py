from crewai import Process
from agent_factory import AgentFactory
from config import Config
from crew_manager import CrewManager
from task_builder import TaskBuilder


class Application:
    """Main application to execute the crew."""

    def __init__(self, use_openai_llm: bool = False):
        self.config = Config()
        self.llm = self.config.get_openai_llm() if use_openai_llm else self.config.get_gemini_llm()
        self.crew_manager = CrewManager()

    def setup(self):
        """Setup the agents and tasks."""
        student = AgentFactory.create_agent(
            role="Grade {grade} student",
            goal="Be a grade {grade} student who are doing homework",
            backstory=(
                "You are a grade {grade} student who is always one of the most genius in the class."
                "You are able to analyze the problem {question} and solve it step-by-step."
                "Your resolution are always neat and clean."
                "Your resolution are comprehensive and easy to understand to other grade {grade} students."
            ),
            allow_delegation=False,
            llm=self.llm,
        )

        teacher = AgentFactory.create_agent(
            role="Grade {grade} teacher",
            goal="Review the student's homework and provide feedback",
            backstory=(
                "You are a grade {grade} teacher who are responsible to review the student's homework."
                "Analyze the student's solution and verify the correctness of each step."
                "Provide feedback to the grade {grade} student to help them understand their mistakes."
                "Provide guidance to the grade {grade} student to help them improve their resolution."
                "Make sure the student's final answer matches {result}."
            ),
            allow_delegation=True,
            llm=self.llm,
        )

        problem_solving_task = TaskBuilder.create_task(
            description=(
                "You are a grade {grade} student. Here is your homework:\n"
                "PROBLEM:\n{question}\n"
                "INSTRUCTIONS:\n"
                "1. Read and understand the problem carefully\n"
                "2. Write down what you know from the problem\n"
                "3. Show your solution step-by-step\n"
                "4. Explain your thinking at each step\n"
                "5. Check your work and verify the answer\n"
                "6. Write your final answer clearly"
            ),
            expected_output=(
                "Please provide your solution in this format:\n"
                "# Understanding the Problem\n"
                "- What we know\n"
                "- What we need to find\n"
                "# Step-by-Step Solution\n"
                "1. First step with explanation\n"
                "2. Second step with explanation\n"
                "(continue with all steps)\n"
                "# Final Answer\n"
                "- Clear statement of the answer\n"
                "- Verification that it makes sense"
            ),
            agent=student,
        )

        homework_reviewing_task = TaskBuilder.create_task(
            description=(
                "You are reviewing a grade {grade} student's homework.\n"
                "ORIGINAL PROBLEM:\n{question}\n"
                "EXPECTED ANSWER:\n{result}\n"
                "REVIEW INSTRUCTIONS:\n"
                "1. Check each step of the student's work\n"
                "2. Verify all calculations are correct\n"
                "3. Ensure the reasoning is grade-appropriate\n"
                "4. Compare their final answer with {result}\n"
                "5. Prepare constructive feedback\n"
                "6. Note any creative approaches they used"
            ),
            expected_output=(
                "Please provide your review in this format:\n\n"
                "# Step-by-Step Review\n"
                "1. Analysis of each step\n"
                "2. Clarity of explanations\n\n"
                "# Feedback\n"
                "- What was done well\n"
                "- Areas for improvement\n"
                "- Specific suggestions\n\n"
                "# Overall Assessment\n"
                "- Final answer correctness\n"
                "- Understanding demonstrated"
            ),
            agent=teacher,
        )

        self.crew_manager.add_agents(student, teacher)
        self.crew_manager.add_tasks(problem_solving_task, homework_reviewing_task)

    def run(self, inputs: dict):
        """Execute the crew and return the result."""
        crew = self.crew_manager.build_crew(
            process=Process.sequential,
            memory=True,
            embedder=self.config.get_google_embedder(),
        )
        result = crew.kickoff(inputs=inputs)
        return result
