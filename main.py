from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/render", response_class=HTMLResponse)
async def render_chat(request: Request, thread: str = Form(...)):
    lines = thread.strip().split("\n")
    messages = []

    for line in lines:
        if line.strip() == "":
            continue
        if line.startswith("You:"):
            messages.append({"side": "right", "text": line[4:].strip()})
        else:
            messages.append({"side": "left", "text": line.strip()})

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "messages": messages
    })
