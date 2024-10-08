from fastapi import FastAPI, Request, APIRouter, HTTPException, Form
from starlette.templating import Jinja2Templates
from typing import Annotated
from starlette.responses import RedirectResponse
from database.db import Session, User, Task
from uuid import UUID
from utils.translations import transform_for_cond
from utils.util import conf_date


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

    db_session = Session()
    users = db_session.query(User).all()
    users = await transform_for_cond(users)

    return templates.TemplateResponse("users/index_users.html", {'request': request, 'data': users})


@router.post("/users")
async def read_user(request: Request):

    db_session = Session()
    users = db_session.query(User).all()
    users = await transform_for_cond(users)

    return templates.TemplateResponse("users/index_users.html", {'request': request, 'data': users})


@router.get("/users/add")
async def add_user(request: Request):
    return templates.TemplateResponse("users/add_user.html", {'request': request})


@router.post("/users/add")
async def add_user(request: Request, fullname: Annotated[str, Form()], telegram_id: Annotated[str, Form()],
                    auth: Annotated[bool, Form()], superuser: Annotated[bool, Form()]):
    
    db_session = Session()
    user = User(fullname=fullname, telegram_id=telegram_id, auth=auth, superuser=superuser)
    db_session.add(user)
    db_session.commit()

    redirect_url = request.url_for("read_user")
    return RedirectResponse(redirect_url)


@router.get("/users/update/{id}")
async def update_user(request: Request, id: UUID):

    db_session = Session()
    user = db_session.query(User).filter(User.id == id).first()

    return templates.TemplateResponse("users/update_user.html", {'request': request, 'user': user})


@router.post("/users/update/{id}")
async def upadte_user(request: Request, id: UUID, fullname: Annotated[str, Form()], auth: Annotated[bool, Form()],
                      superuser: Annotated[bool, Form()]):
    
    db_session = Session()
    db_session.query(User).filter(User.id == id).update({'fullname': fullname, 'auth': auth,
                                                          'superuser': superuser})
    db_session.commit()
    
    redirect_url = request.url_for("read_user")
    return RedirectResponse(redirect_url)


@router.get("/users/delete/{id}")
async def delete_user(request: Request, id: UUID):

    db_session = Session()
    user = db_session.query(User).filter(User.id == id).first()
    db_session.delete(user)
    db_session.commit()

    redirect_url = request.url_for("read_user")
    return RedirectResponse(redirect_url)



@router.get("/tasks")
async def read_tasks(request: Request):

    db_session = Session()
    tasks = db_session.query(Task).all()

    return templates.TemplateResponse("tasks/index_tasks.html", {'request': request, 'data': tasks})


@router.post("/tasks")
async def read_tasks(request: Request):

    db_session = Session()
    tasks = db_session.query(Task).all()

    return templates.TemplateResponse("tasks/index_tasks.html", {'request': request, 'data': tasks})


@router.get("/tasks/add")
async def add_tasks(request: Request):
    return templates.TemplateResponse("tasks/add_tasks.html", {'request': request})


@router.post("/tasks/add")
async def add_tasks(request: Request, subject: Annotated[str, Form()], type: Annotated[str, Form()],
                    task: Annotated[str, Form()], date: Annotated[str, Form()]):
    
    db_session = Session()
    task = Task(subject=subject, type=type, task=task, date=await conf_date(date))
    db_session.add(task)
    db_session.commit()

    redirect_url = request.url_for("read_tasks")
    return RedirectResponse(redirect_url)


@router.get("/tasks/update/{id}")
async def update_tasks(request: Request, id: UUID):

    db_session = Session()
    task = db_session.query(Task).filter(Task.id == id).first()

    return templates.TemplateResponse("tasks/update_tasks.html", {'request': request, 'task': task})


@router.post("/tasks/update/{id}")
async def update_tasks(request: Request, id: UUID, subject: Annotated[str, Form()], type: Annotated[str, Form()],
                       task: Annotated[str, Form()], date: Annotated[str, Form()]):
    
    db_session = Session()
    db_session.query(Task).filter(Task.id == id).update({'subject': subject, 'type': type,
                                                         'task': task, 'date': await conf_date(date)})
    db_session.commit()

    redirect_url = request.url_for("read_tasks")
    return RedirectResponse(redirect_url)


@router.get("/tasks/delete/{id}")
async def delete_tasks(request: Request, id: UUID):

    db_session = Session()
    task = db_session.query(Task).filter(Task.id == id).first()
    db_session.delete(task)
    db_session.commit()

    redirect_url = request.url_for("read_tasks")
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
