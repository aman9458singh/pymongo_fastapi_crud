from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from config.db import conn
from schema.note import noteEntity, notesEntity
from fastapi.templating import Jinja2Templates

note= APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.fastapi.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id":doc["_id"],
            "title":doc["title"],
            "desc":doc["desc"],
        })
    return templates.TemplateResponse("index.html", {"request":request , "newDocs": newDocs})


@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    formDict = dict(form)
    note= conn.fastapi.notes.insert_one(formDict) 
    return {"success":True}
