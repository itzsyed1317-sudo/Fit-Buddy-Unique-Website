from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
import os

from .database import init_db, get_db, User
from .schemas import UserInput
from .gemini_service import generate_workout, generate_tip, update_workout

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="FitBuddy — Pulse Edition",
    version="2.0"
)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/generate-workout", response_class=HTMLResponse)
def generate(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    data = UserInput(
        user_id=user_id,
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    plan, source = generate_workout(
        data.name,
        data.age,
        data.weight,
        data.goal,
        data.intensity
    )

    tip, tip_source = generate_tip(data.goal)

    user = (
        db.query(User)
        .filter(User.user_id == data.user_id)
        .first()
    )

    if user:
        user.name = data.name
        user.age = data.age
        user.weight = data.weight
        user.goal = data.goal
        user.intensity = data.intensity
        user.original_plan = plan
        user.updated_plan = None
        user.feedback = None
        user.nutrition_tip = tip

    else:
        user = User(
            user_id=data.user_id,
            name=data.name,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity,
            original_plan=plan,
            nutrition_tip=tip
        )

        db.add(user)

    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "plan": plan,
            "tip": tip,
            "source": source,
            "tip_source": tip_source,
            "updated": False
        }
    )


@app.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not user:
        return RedirectResponse(
            "/",
            status_code=303
        )

    revised, source = update_workout(
        user.original_plan,
        feedback,
        user.goal,
        user.intensity
    )

    user.updated_plan = revised
    user.feedback = feedback

    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "plan": revised,
            "tip": user.nutrition_tip,
            "source": source,
            "tip_source": "Stored",
            "updated": True
        }
    )


@app.get("/admin", response_class=HTMLResponse)
def admin(
    request: Request,
    db: Session = Depends(get_db)
):
    users = (
        db.query(User)
        .order_by(desc(User.created_at))
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "users": users
        }
    )


@app.post("/admin/delete/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user:
        db.delete(user)
        db.commit()

    return RedirectResponse(
        "/admin",
        status_code=303
    )