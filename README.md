FastAPI To-Do App - Week 1 Progress

Description: Simple ToDo API built in FastAPI. Intended to assist in learning the basic structure of FastAPI endpoints.

Setup:
# Clone the repository
git clone fastapi-todo

# Navigate to the project directory
cd fastapi-todo

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
