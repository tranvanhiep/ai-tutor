import warnings
import random
import argparse
from IPython.display import Markdown

from app.application import Application
from enums.llm_type import LLMType
from utils.csv_reader import CSVReader

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

if __name__ == "__main__":
    args = parse_args()
    warnings.filterwarnings('ignore')

    # Read problems from specified file
    csv_reader = CSVReader(args.file)
    problems = csv_reader.read_to_dict()

    # Pick one random problem
    problem = random.choice(problems)

    print(f"Question ID: {problem['item_id']}")
    print(f"Description: {problem['item_description']}")
    print(f"Question: {problem['question']}")
    print(f"Answer: {problem['answer']}")
    print(f"Explanation: {problem['explanation']}\n")

    inputs = {
        "grade": 7,
        "question": "\n".join([problem["item_description"], problem["question"]]),
        "explanation": problem["explanation"],
        "answer": problem["answer"],
    }

    app = Application(llm_type=LLMType[args.llm])
    app.setup(total_students=args.students)
    result = app.run(inputs)
    Markdown(result.raw)
