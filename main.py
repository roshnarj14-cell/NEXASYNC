import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import init_db
import auth, dashboard, styles, samples, qa, dispatch, brands, merchants, users, wash

app = FastAPI(title="Aquarelle India PLM")
app.add_middleware(SessionMiddleware, secret_key="aquarelle-plm-secret-2025")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    init_db()

for r in [auth, dashboard, styles, samples, qa, dispatch, brands, merchants, users, wash]:
    app.include_router(r.router)

@app.get("/")
def root():
    return RedirectResponse("/login", 302)
