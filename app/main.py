from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func
from .db import Base, engine, get_db
from .models import Category, Budget, Expense
from fastapi.responses import RedirectResponse

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
    categories = db.query(Category).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "categories": categories, "alert": alert})

@app.post("/expense/add")
def add_expense(category: int = Form(...), amount: float = Form(...), note: str = Form(""), db: Session = Depends(get_db)):
    e = Expense(category_id=category, amount=amount, note=note)
    db.add(e); db.commit()

    now = datetime.now()
    spent = db.query(func.sum(Expense.amount)).filter(
        Expense.category_id==category,
        func.extract('month',Expense.created_at)==now.month,
        func.extract('year',Expense.created_at)==now.year
    ).scalar() or 0

    budget = db.query(Budget.amount).filter(
        Budget.category_id==category,
        Budget.month==now.month,
        Budget.year==now.year
    ).scalar()

    alert=None
    if budget and spent > budget: alert="Budget exceeded!"

    return RedirectResponse("/dashboard"+(f"?alert={alert}" if alert else ""),303)

@app.post("/budget/set")
def set_budget(category:int=Form(...),amount:float=Form(...),db:Session=Depends(get_db)):
    now=datetime.now()
    b=db.query(Budget).filter(Budget.category_id==category,Budget.month==now.month,Budget.year==now.year).first()
    if b: b.amount=amount
    else: db.add(Budget(category_id=category,amount=amount,month=now.month,year=now.year))
    db.commit()
    return RedirectResponse("/dashboard",303)

@app.get("/report", response_class=HTMLResponse)
def report(request:Request,db:Session=Depends(get_db)):
    now=datetime.now()
    total=db.query(func.sum(Expense.amount)).filter(
        func.extract('month',Expense.created_at)==now.month,
        func.extract('year',Expense.created_at)==now.year
    ).scalar() or 0

    rows=[]
    for c in db.query(Category).all():
        spent=db.query(func.sum(Expense.amount)).filter(
            Expense.category_id==c.id,
            func.extract('month',Expense.created_at)==now.month,
            func.extract('year',Expense.created_at)==now.year
        ).scalar() or 0
        budget=db.query(Budget.amount).filter(
            Budget.category_id==c.id,Budget.month==now.month,Budget.year==now.year
        ).scalar()
        rows.append({"category":c.name,"budget":float(budget) if budget else None,"spent":float(spent),"remaining":float(budget-spent) if budget else None})
    return templates.TemplateResponse("report.html",{"request":request,"total_spent":float(total),"rows":rows})
