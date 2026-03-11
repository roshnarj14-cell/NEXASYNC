from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=".")
def get_user(r): return r.session.get("user")

@router.get("/wash", response_class=HTMLResponse)
def wash_page(request: Request):
    user = get_user(request)
    if not user: return RedirectResponse("/login", 302)
    from main_controller import WashController
    records = WashController().get_all()
    return templates.TemplateResponse("wash.html", {"request": request, "user": user, "active": "wash", "records": records})

@router.post("/wash/create")
def wash_create(request: Request, style_code: str = Form(""), customer: str = Form(""),
    season: str = Form(""), color: str = Form(""), wash_type: str = Form("BASIC"),
    result: str = Form("Pending"), sent_date: str = Form(""), received_date: str = Form(""),
    comments: str = Form("")):
    user = get_user(request)
    if not user: return RedirectResponse("/login", 302)
    from main_controller import WashController
    WashController().create({
        "sample_id": None, "style_code": style_code, "customer": customer,
        "merchant": "", "season": season, "color": color, "fabric_type": "",
        "sample_type": "", "wash_type": wash_type, "required_wash": "",
        "wash_unit": "", "sent_date": sent_date or None, "received_date": received_date or None,
        "result": result, "comments": comments, "created_by": user["id"]
    })
    return RedirectResponse("/wash", 302)

@router.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request):
    user = get_user(request)
    if not user: return RedirectResponse("/login", 302)
    return templates.TemplateResponse("reports.html", {"request": request, "user": user, "active": "reports"})
