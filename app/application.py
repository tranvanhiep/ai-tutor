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

    def setup(self, total_students: int = 100):
        """Setup the agents and tasks.

        This method initializes the AI tutor system by creating student agents and a teacher agent,
        along with their associated tasks for problem solving and homework reviewing.

        Args:
            total_students (int, optional): The number of student agents to create. Defaults to 100.
                Each student agent will be assigned a problem solving task.
        """
        problem_solving_tasks: list[Task] = []
        students: list[Agent] = []
        for _ in range(total_students):
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
                    "Please provide your submission in this format:\n"
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
                async_execution=True,
            )

            students.append(student)
            problem_solving_tasks.append(problem_solving_task)

        teacher = AgentFactory.create_agent(
            role="Grade {grade} teacher",
            goal="Review the student's submissions and provide feedback",
            backstory=(
                "You are a grade {grade} teacher who are responsible to review the student's submissions."
                "Analyze the student's solutions and verify the correctness of each step."
                "Make sure the final answer is correct and the reasoning is grade-appropriate."
                "Provide feedback to the grade {grade} student to help them understand their mistakes."
                "Provide guidance to the grade {grade} student to help them improve their resolution."
            ),
            allow_delegation=True,
            llm=self.llm,
        )

        homework_reviewing_task = TaskBuilder.create_task(
            description=(
                "You are reviewing all of the grade {grade} student's submissions.\n"
                "ORIGINAL PROBLEM:\n{question}\n"
                "REVIEW INSTRUCTIONS:\n"
                "1. Check each step of the student's work\n"
                "2. Verify all calculations are correct\n"
                "3. Ensure the reasoning is grade-appropriate\n"
                "4. Make sure their final answer is correct\n"
                "5. Prepare constructive feedback\n"
                "6. Note any creative approaches they used\n"
            ),
            expected_output=(
                "Please provide your review of submission in this format:\n\n"
                "# Student submission\n"
                "- Display student submission here for reference\n"
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

        pick_solution_task = TaskBuilder.create_task(
            description=(
                "You are the grade {grade} teacher.\n"
                "Based on your review, you need to choose the most accurate "
                "and grade-appropriate submission among submissions.\n"
            ),
            expected_output=(
                "Please provide the most accurate and grade-appropriate submission in this format:\n\n"
                "# Most Accurate And Grade-appropriate Solution\n"
                "- Display the student step-by-step solution with explanation here\n"
                "# Justification\n"
                "- Explain why you choose this solution\n"
            ),
            agent=teacher,
        )

        # Add Marker agent
        marker = AgentFactory.create_agent(
            role="Grade {grade} marker",
            goal="Verify student solutions against the correct answer",
            backstory=(
                "You are an expert marker for grade {grade}.\n"
                "Your role is to verify if student solutions match the expected answer {answer}.\n"
                "You have deep understanding of multiple solution approaches.\n"
                "You can determine if different solution methods arrive at equivalent results.\n"
                "You are extremely detail-oriented and catch even minor calculation errors."
            ),
            allow_delegation=False,
            llm=self.llm,
        )

        verify_solution_task = TaskBuilder.create_task(
            description=(
                "As a grade {grade} marker, verify the chosen solution against the correct answer.\n"
                "CORRECT ANSWER: {answer}\n"
                "VERIFICATION INSTRUCTIONS:\n"
                "1. Check if the final answer matches exactly\n"
                "2. If different, determine if it's equivalent\n"
                "3. Verify all calculations in the solution\n"
                "4. Check if the solution method is valid\n"
                "5. Note any discrepancies found"
            ),
            expected_output=(
                "Please provide your verification in this format:\n\n"
                "# Answer Verification\n"
                "- Expected Answer: {answer}\n"
                "- Student's Answer: [extract from solution]\n"
                "- Equivalence Status: [Exact Match/Equivalent/Incorrect]\n\n"
                "# Calculation Check\n"
                "- All calculations verified: [Yes/No]\n"
                "- Errors found: [List any errors]\n\n"
                "# Method Validation\n"
                "- Solution method: [Valid/Invalid]\n"
                "- Mathematical rigor: [Assessment]\n\n"
                "# Final Verdict\n"
                "- [CORRECT/INCORRECT]\n"
                "- Detailed justification"
            ),
            agent=marker,
        )

        self.crew_manager.add_agents(*students, teacher, marker)
        self.crew_manager.add_tasks(
            *problem_solving_tasks,
            homework_reviewing_task,
            pick_solution_task,
            verify_solution_task
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
