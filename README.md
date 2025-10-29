# Expense Tracker Application

- This application helps users track expenses and set monthly budgets for categories with a global filter in YYYY-MM format on dashboard screen.
- Report screen displays monthly expenses along with grouped monthly data category-wise.

✨ Features

- Add daily expenses with categories

- Set monthly budgets per category (update if exists)

- Alert when spending exceeds budget

- View monthly reports: total & per-category breakdown

- Predefined categories: Food, Transport, Entertainment, Other

- FastAPI backend with Jinja2 HTML UI

- Can run locally or inside Docker

🛠 Tech Stack

- FastAPI

- PostgreSQL

- SQLAlchemy ORM

- Jinja2 Templates

- Docker 


# 🚀 Run the Project Locally
- git clone https://github.com/AbhishekKumar567/expense-tracker-assignment.git

- cd expense-tracker-fastapi

1) Create a virtual environment

 Windows:

 - python -m venv venv
 - venv\Scripts\activate

 Mac/Linux:

 - python3 -m venv venv
 - source venv/bin/activate

2) Install dependencies:
- pip install -r requirements.txt

3) Create PostgreSQL database:
- CREATE DATABASE expense_tracker;

4) Create .env file in project root:
- DATABASE_URL=postgresql://username:password@localhost:5432/expense_tracker

5) Start the FastAPI server:
- uvicorn app.main:app --reload

# 🐳 Run using Docker
 Build image:

- docker build -t expense-tracker .

Make sure PostgreSQL is running on host & .env exists:

- DATABASE_URL=postgresql://username:password@localhost:5432/expense_tracker

Run container:

- docker run -p 8000:8000 --env-file .env expense-tracker

- Visit in browser:
http://127.0.0.1:8000
