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
python main.py --llm GOOGLE --students 10 --file data/question_content_math_7.csv
```

### Command Line Arguments

- `--llm`: Choose LLM backend (GOOGLE, OPENAI, or LOCAL)
- `--students`: Number of student agents to simulate (default: 10)
- `--file`: Path to CSV file containing math problems

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
3. Have the teacher review solutions
4. Verify answer correctness
5. Provide detailed feedback
