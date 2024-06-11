# main.py

from fastapi import FastAPI, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from . import models, schemas, crud
from .database import engine, get_db
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="crud_jinja_app/templates")
app.mount("/static", StaticFiles(directory="crud_jinja_app/static"), name="static")

@app.get("/")
def read_items(request: Request, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.get("/items/create/")
def create_item_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/items/create/")
def create_item(request: Request, title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    item = schemas.ItemCreate(title=title, description=description)
    crud.create_item(db=db, item=item)
    return RedirectResponse(url="/", status_code=303)

@app.get("/items/update/{item_id}")
def update_item_form(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("update.html", {"request": request, "item": item})

@app.post("/items/update/{item_id}")
def update_item(request: Request, item_id: int, title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    item = schemas.ItemCreate(title=title, description=description)
    updated_item = crud.update_item(db=db, item_id=item_id, item=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return RedirectResponse(url="/", status_code=303)

@app.post("/items/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted_item = crud.delete_item(db=db, item_id=item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return RedirectResponse(url="/", status_code=303)
