import warnings
import os
from datetime import datetime
from IPython.display import Markdown

from app.application import Application
from enums.llm_type import LLMType
from utils.csv_reader import CSVReader
from utils.html_to_text import HTMLToText
from utils.parse_args import parse_args
from utils.markdown_writer import MarkdownWriter

# Create results directory if it doesn't exist
OUTPUT_DIR = 'output'

if __name__ == "__main__":
    args = parse_args()
    warnings.filterwarnings('ignore')

    question_text = None
    answer_text = None
    question_image = None
    answer_image = None

    # Read problems from specified file
    csv_reader = CSVReader(args.file)
    problems = csv_reader.read_to_dict()

    # Initialize markdown writer
    md_writer = MarkdownWriter(OUTPUT_DIR)

    for problem in problems:
        if args.enable_converter:
            # Initialize HTML to text converter
            converter = HTMLToText()

            try:
                # Process question and answer
                question_text, question_image = converter.process_content(
                    problem, 'question', problem['item_id'])
                answer_text, answer_image = converter.process_content(
                    problem, 'answer', problem['item_id'])
            except ValueError as e:
                print(f"Error processing content: {e}")
                # Cleanup any temporary files that might have been created
                if question_image:
                    HTMLToText.cleanup_temp_files(question_image)
                if answer_image:
                    HTMLToText.cleanup_temp_files(answer_image)
                exit(1)
        else:
            # Use raw content without conversion
            question_text = f"{problem['item_description']}\n{problem['question']}"
            answer_text = problem['answer']

        # Update the inputs dictionary
        inputs = {
            "grade": 7,
            "question": question_text,
            "explanation": problem["explanation"],
            "answer": answer_text,
        }

        print(f"Question ID: {problem['item_id']}")
        print(f"Question: {question_text}")
        print(f"Answer: {answer_text}")
        print(f"Explanation: {problem['explanation']}\n")

        app = Application(llm_type=LLMType[args.llm])
        app.setup(total_students=args.students)
        result = app.run(inputs)

        # Write results to markdown file
        try:
            md_writer.write_problem_result(
                problem_id=problem['item_id'],
                question=question_text,
                answer=answer_text,
                analysis=result.raw
            )
        except IOError as e:
            print(f"Error writing results: {e}")
            if question_image:
                HTMLToText.cleanup_temp_files(question_image)
            if answer_image:
                HTMLToText.cleanup_temp_files(answer_image)
            exit(1)

        # Display result in notebook
        Markdown(result.raw)

        # Cleanup temporary files
        if question_image:
            HTMLToText.cleanup_temp_files(question_image)
        if answer_image:
            HTMLToText.cleanup_temp_files(answer_image)
