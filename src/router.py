import json
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.service import validate_obj, RecordCRUD
from src.models import Record

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/upload', response_class=HTMLResponse)
async def form_upload(request: Request):
    return templates.TemplateResponse(
        "upload.html", {"request": request}
    )


@router.post('/upload', response_class=HTMLResponse)
async def handle_upload(
    request: Request,
    file: UploadFile = File(...)
):
    print("Post upload")

    content = await file.read()
    data = json.loads(content)
    validate_bools = list(map(validate_obj, data))
    if False not in validate_bools:
        for obj in data:
            rec = Record(
                name=obj['name'],
                date=obj['date']
            )
            await RecordCRUD.create(rec)
    else:
        return templates.TemplateResponse("upload.html", {
            "request": request, "error": "Неверный JSON"
        })

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "success": f"Принято {file.filename}, размер {len(content)} байт"
    })


@router.get('/records', response_class=HTMLResponse)
async def get_all_records(request: Request):
    records = await RecordCRUD.get_all()
    return templates.TemplateResponse("records.html", {"request": request, "records": records})