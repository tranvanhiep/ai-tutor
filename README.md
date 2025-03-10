# AI Tutor System

An intelligent tutoring system that simulates student-teacher interactions for mathematics problem solving using AI agents.

## Overview

This project implements an AI-based tutoring system where:
- Multiple student agents solve math problems independently
- A teacher agent reviews and provides feedback on solutions
- A marker agent verifies solution correctness
- The system supports multiple LLM backends (Google, OpenAI, or Local)

# Prerequisites

1. Install Miniconda:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
2. Create and activate a new conda environment:
```bash
conda create -n ai-tutor python=3.12.3
conda activate ai-tutor
```

3. Install system dependencies:
```bash
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-jpn
```

## Installation

1. Clone the repository:
```bash
git clone git@github.com:tranvanhiep/ai-tutor.git
cd ai-tutor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` file with your API keys and configuration.

## Usage

Run the application using main.py:

```bash
python main.py --llm GOOGLE --students 10 --file data/question_content_math_7.csv --enable-converter
```

### Command Line Arguments

The application accepts the following command line arguments:

| Argument | Description | Type | Default | Values |
|----------|-------------|------|---------|---------|
| `--llm` | LLM type to use | string | `GOOGLE` | `GOOGLE`, `OPENAI`, `LOCAL` |
| `--students` | Number of students to simulate | integer | `10` | Any positive integer |
| `--file` | Path to CSV file containing problems | string | `data/question_content_math_7.csv` | Valid file path |
| `--enable-converter` | Enable HTML to text conversion for math content | boolean | `False` | `True` when flag present |

### Example Usage

```bash
# Run with default settings
python main.py

# Run with OpenAI and 5 students
python main.py --llm OPENAI --students 5

# Run with HTML conversion enabled
python main.py --enable-converter

# Run with custom problem set and HTML conversion
python main.py --file custom_problems.csv --enable-converter
```

## Project Structure

- app: Core application logic and agent implementations
- config: Configuration and LLM setup
- data: Math problem datasets
- enums: Enumerations for LLM types
- utils: Utility functions and helpers

## Key Components

- `Application`: Main application class orchestrating the tutoring process
- `AgentFactory`: Creates student, teacher, and marker agents
- `CrewManager`: Manages agent interactions and task execution
- `TaskBuilder`: Constructs tasks for agents

## Sample Output

The system will:
1. Load a random math problem
2. Generate student solutions
3. Verify answer correctness
4. Provide detailed feedback
