# FitBuddy — Pulse Edition

A redesigned FitBuddy AI fitness-plan web application built with FastAPI, Jinja2, SQLAlchemy/SQLite, and Gemini.

## Features
- Modern responsive Aurora/Pulse frontend
- Personalized 7-day workout plan generation
- Nutrition/recovery tip
- Feedback-based plan regeneration
- SQLite persistence
- Admin dashboard with user and plan history
- Gemini integration
- Safe demo fallback when no Gemini key is configured

## Project structure

```text
FitBuddy_Unique/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── gemini_service.py
│   └── schemas.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   └── admin.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── data/
├── .env.example
├── requirements.txt
└── README.md
```

## Run on Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/admin
- http://127.0.0.1:8000/docs

## Gemini
Put your key in `.env`:

```env
GOOGLE_API_KEY=AQ.Ab8RN6KYS--CAJlqkh66gfDQXcOujN92lRXkVpxuRsgfpzpsIQ
```

The app tries Gemini when a key is available. If it cannot call Gemini, it uses a clearly labeled local demo generator so the UI can still be tested.

## Demo Video
(https://drive.google.com/file/d/14VsJYG8q9sNzQmzCCUqW9ZVaryoMSAk_/view?usp=sharing)
