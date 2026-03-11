from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=".")

def get_user(r): return r.session.get("user")

@router.get("/dispatch", response_class=HTMLResponse)
def dispatch_page(request: Request, tab: str = "history"):
    user = get_user(request)
    if not user: return RedirectResponse("/login", 302)
    from main_controller import DispatchController, SampleController
    dispatches = DispatchController.get_all()
    pending = SampleController.get_all(filters={"status": "Approved"})
    return templates.TemplateResponse("dispatch.html", {"request": request, "user": user, "active": "dispatch", "tab": tab, "dispatches": dispatches, "pending": pending})

@router.post("/dispatch/submit")
def dispatch_submit(request: Request, sample_db_id: int = Form(...),
    recipient: str = Form(...), address: str = Form(""),
    courier: str = Form(""), tracking_no: str = Form(""), notes: str = Form("")):
    user = get_user(request)
    if not user: return RedirectResponse("/login", 302)
    from main_controller import DispatchController
    DispatchController.dispatch_sample(sample_db_id, recipient, address, courier, tracking_no, user["id"], notes)
    return RedirectResponse("/dispatch", 302)
