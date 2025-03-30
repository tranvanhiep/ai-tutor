import os
from datetime import datetime


class MarkdownWriter:
    """A utility class to handle writing Markdown files."""

    def __init__(self, output_dir: str):
        """
        Initialize MarkdownWriter with output directory.
        Creates the directory if it doesn't exist.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def write_problem_result(
        self,
        problem_id: str,
        question: str,
        answer: str,
        analysis: str,
    ) -> str:
        """
        Write problem results to a Markdown file.

        Args:
            problem_id: Problem identifier
            question: Problem question text
            answer: Problem answer text
            analysis: Analysis/results text

        Returns:
            str: Path to the created file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{problem_id}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        content = [
            f"# Problem {problem_id} Results\n",
            "## Question\n",
            f"{question}\n",
            "## Answer\n",
            f"{answer}\n",
            "## Analysis\n",
            f"{analysis}\n"
        ]

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(content)
            return filepath
        except IOError as e:
            raise IOError(f"Error writing markdown file: {str(e)}")
