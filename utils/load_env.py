from dotenv import find_dotenv, load_dotenv


def load_env():
    """Load environment variables from .env file"""
    load_dotenv(find_dotenv())
