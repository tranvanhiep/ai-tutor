import argparse

def parse_args():
    """
    Parse command line arguments for the AI Tutor application.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
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
    parser.add_argument(
        '--enable-converter',
        action='store_true',
        default=False,
        help='Enable HTML to text conversion (default: False)'
    )
    return parser.parse_args()
