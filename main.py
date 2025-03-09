import warnings
import random
import argparse
from IPython.display import Markdown

from app.application import Application
from enums.llm_type import LLMType
from utils.csv_reader import CSVReader
from utils.html_to_text import HTMLToText


def parse_args():
    parser = argparse.ArgumentParser(description='AI Tutor Application')
    parser.add_argument(
        '--llm',
        type=str,
        choices=['GOOGLE', 'OPENAI', 'LOCAL'],
        default='GOOGLE',
        help='LLM type to use (GOOGLE or OPENAI or LOCAL)'
    )
    parser.add_argument(
        '--students',
        type=int,
        default=10,
        help='Number of students to simulate'
    )
    parser.add_argument(
        '--file',
        type=str,
        default='data/question_content_math_7.csv',
        help='Path to CSV file containing problems'
    )
    return parser.parse_args()


# Update main section
if __name__ == "__main__":
    args = parse_args()
    warnings.filterwarnings('ignore')

    # Initialize HTML to text converter
    converter = HTMLToText()

    # Read problems from specified file
    csv_reader = CSVReader(args.file)
    problems = csv_reader.read_to_dict()

    # Pick one random problem
    problem = random.choice(problems)

    # Initialize image variables
    question_image = None
    answer_image = None

    try:
        # Process question and answer
        question_text, question_image = converter.process_content(problem, 'question', problem['item_id'])
        answer_text, answer_image = converter.process_content(problem, 'answer', problem['item_id'])
    except ValueError as e:
        print(f"Error processing content: {e}")
        # Cleanup any temporary files that might have been created
        if 'question_image' in locals() and question_image:
            HTMLToText.cleanup_temp_files(question_image)
        if 'answer_image' in locals() and answer_image:
            HTMLToText.cleanup_temp_files(answer_image)
        exit(1)

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
    Markdown(result.raw)

    # Cleanup temporary files
    if question_image:
        HTMLToText.cleanup_temp_files(question_image)
    if answer_image:
        HTMLToText.cleanup_temp_files(answer_image)
