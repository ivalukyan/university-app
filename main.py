from fastapi import FastAPI, Request, APIRouter, HTTPException, Form
from starlette.templating import Jinja2Templates
from typing import Annotated
from starlette.responses import RedirectResponse


app = FastAPI(
    title='University'
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@router.post("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})


@router.get("/users")
async def read_user(request: Request):
    return templates.TemplateResponse("users/index_users.html", {'request': request})


@router.get("/tasks")
async def read_tasks(request: Request):
    return templates.TemplateResponse("tasks/index_tasks.html", {'request': request})


@router.get("/sends")
async def sends_message(request: Request):
    return templates.TemplateResponse("sends/index_sends.html", {'request': request})


@router.post("/sends")
async def sends_message(request: Request, message: Annotated[str, Form()]):
    redirect_url = request.url_for("home")
    return RedirectResponse(redirect_url)


app.include_router(router)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/404.html", {"request": request, 'exception': exp})


@app.exception_handler(500)
async def custom_500_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/500.html", {"request": request, 'exception': exp})


@app.exception_handler(400)
async def custom_400_handler(request: Request, exp: HTTPException):
    return templates.TemplateResponse("exception_handler/400.html", {"request": request, 'exception': exp})
