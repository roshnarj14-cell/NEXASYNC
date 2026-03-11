from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=".")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", 302)
    from main_controller import DashboardController
    stats = DashboardController.get_stats()
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "stats": stats, "active": "dashboard"})
