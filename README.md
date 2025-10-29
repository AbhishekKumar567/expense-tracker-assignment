Expense Tracker — FastAPI + PostgreSQL + HTML

This application helps users track expenses and set monthly budgets by category.

Features

Add daily expenses with categories

Set monthly budgets per category (updates if already exists)

Alert when spending exceeds budget

View monthly report: total and per-category breakdown

Predefined categories: Food, Transport, Entertainment, Other

Uses FastAPI with Jinja2 templates (HTML UI)

Supports running via local environment or Docker

Tech Stack

FastAPI

PostgreSQL

SQLAlchemy ORM

Jinja2 Templates

Docker (optional)

Run the Project Locally

- git clone https://github.com/your-username/expense-tracker-fastapi.git
- cd expense-tracker-fastapi

Create virtual environment

For windows 
python -m venv venv
venv\Scripts\activate

For mac/linux
python3 -m venv venv
source venv/bin/activate

install dependencies:
pip install -r requirements.txt

Create PostgreSQL database:
CREATE DATABASE expense_tracker

Create .env file:
DATABASE_URL=postgresql://username:password@localhost:5432/expense_tracker

Start server:
uvicorn app.main:app --reload





  

