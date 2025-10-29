from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from .db import Base, engine, get_db
from .models import Category, Budget, Expense

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)

def seed_categories(db: Session):
    names = ["Food", "Transport", "Entertainment", "Other"]
    if db.query(Category).count() == 0:
        for n in names:
            db.add(Category(name=n))
        db.commit()

with next(get_db()) as db:
    seed_categories(db)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/dashboard")


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, alert: str = None, db: Session = Depends(get_db)):
    period = request.query_params.get("period") or datetime.now().strftime("%Y-%m")
    categories = db.query(Category).all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "categories": categories,
        "alert": alert,
        "period": period
    })


@app.post("/expense/add")
def add_expense(
    request: Request,
    category: int = Form(...),
    amount: float = Form(...),
    note: str = Form(""),
    db: Session = Depends(get_db)
):
    # Read from query (sticky) else default
    period = request.query_params.get("period") or datetime.now().strftime("%Y-%m")

    e = Expense(category_id=category, amount=amount, note=note, period=period)
    db.add(e); db.commit()

    spent = db.query(func.sum(Expense.amount)).filter(
        Expense.category_id == category,
        Expense.period == period
    ).scalar() or 0

    budget = db.query(Budget.amount).filter(
        Budget.category_id == category,
        Budget.period == period
    ).scalar()

    alert = None
    if budget and spent > budget:
        alert = "Budget exceeded!"

    redirect_url = f"/dashboard?period={period}"
    if alert: redirect_url += f"&alert={alert}"

    return RedirectResponse(redirect_url, 303)


@app.post("/budget/set")
def set_budget(
    request: Request,
    category: int = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db)
):
    period = request.query_params.get("period") or datetime.now().strftime("%Y-%m")

    b = db.query(Budget).filter(Budget.category_id == category, Budget.period == period).first()
    if b:
        b.amount = amount
    else:
        db.add(Budget(category_id=category, amount=amount, period=period))
    db.commit()

    return RedirectResponse(f"/dashboard?period={period}", 303)


@app.get("/report", response_class=HTMLResponse)
def report(request: Request, db: Session = Depends(get_db)):

    # 1) Get all unique periods from Budget or Expense
    periods = db.query(Expense.period).distinct().all()
    periods = sorted({p[0] for p in periods})   # set + sorted

    grouped = []

    for period in periods:
        # Total spent for this month
        total = db.query(func.sum(Expense.amount)).filter(
            Expense.period == period
        ).scalar() or 0

        rows = []
        for c in db.query(Category).all():
            spent = db.query(func.sum(Expense.amount)).filter(
                Expense.category_id == c.id,
                Expense.period == period
            ).scalar() or 0

            budget = db.query(Budget.amount).filter(
                Budget.category_id == c.id,
                Budget.period == period
            ).scalar()

            rows.append({
                "category": c.name,
                "budget": float(budget) if budget else None,
                "spent": float(spent),
                "remaining": float(budget - spent) if budget else None
            })

        grouped.append({
            "period": period,
            "total_spent": float(total),
            "rows": rows
        })

    return templates.TemplateResponse(
        "report.html",
        {"request": request, "grouped": grouped}
    )

