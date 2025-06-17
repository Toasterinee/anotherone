# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.database import engine, get_db
from app.models import Base, Application
from app.schemas import ApplicationForm
from pydantic import ValidationError
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Константы для базовой аутентификации
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_secure_password"  # Замените на свой пароль

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["Staticimages"] = "/app/static/images"

# Сначала определяем маршрут для удаления
@app.delete("/admin/application/{application_id}")
async def delete_application(
    application_id: int,
    credentials: HTTPBasicCredentials = Depends(verify_credentials),
    db: Session = Depends(get_db)
):
    print(f"Попытка удаления заявки с ID: {application_id}")  # Отладочная информация
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        print(f"Заявка с ID {application_id} не найдена")  # Отладочная информация
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    
    print(f"Удаление заявки с ID: {application_id}")  # Отладочная информация
    db.delete(application)
    db.commit()
    return {"status": "success", "message": "Заявка успешно удалена"}

# Затем определяем остальные маршруты
@app.get("/", response_class=HTMLResponse)
async def get_form():
    template = templates.get_template("index.html")
    return template.render()

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(credentials: HTTPBasicCredentials = Depends(verify_credentials), db: Session = Depends(get_db)):
    applications = db.query(Application).order_by(Application.created_at.desc()).all()
    template = templates.get_template("admin.html")
    return template.render(applications=applications, admin_password=ADMIN_PASSWORD)

@app.post("/submit")
async def submit_form(
        full_name: str = Form(...),
        phone: str = Form(...),
        message: str = Form(...),
        agreement: bool = Form(False),
        db: Session = Depends(get_db)
):
    try:
        # Валидация через Pydantic
        form_data = ApplicationForm(
            full_name=full_name,
            phone=phone,
            message=message,
            agreement=agreement
        )

        # Сохранение в базу данных
        db_application = Application(
            full_name=form_data.full_name,
            phone=form_data.phone,
            message=form_data.message,
            agreement=form_data.agreement
        )
        db.add(db_application)
        db.commit()
        db.refresh(db_application)

        return JSONResponse(content={"status": "success", "message": "Заявка успешно отправлена!"})

    except ValidationError as e:
        # Извлекаем сообщения об ошибках
        error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        error_message = "; ".join(error_messages)
        return JSONResponse(
            content={"status": "error", "message": error_message},
            status_code=422
        )