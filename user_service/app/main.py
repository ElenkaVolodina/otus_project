import bcrypt
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app import jwt, storage
from app.forms.user import UserCreateForm
from app.schemas.user import UserCreate, UserUpdate
from app.utils import user as user_utils

app = FastAPI(
    title="OTUS HomeWork #5",
    version="1",
)

jwt.setup_jwk(app)
storage.setup_storage(app, app.private_key)


templates = Jinja2Templates(directory="app/templates/")


@app.get("/registration")
async def registration_form(request: Request):
    return templates.TemplateResponse('registration.jinja2', context={'request': request})


@app.post("/registration")
async def registration_form(request: Request):
    form = UserCreateForm(request)
    await form.load_data()
    if form.is_valid():
        print(await request.form())
        user = UserCreate(** await request.form())
        db_user = await user_utils.get_user_by_username(username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf8')
        await user_utils.create_user(user=user)
        redirect_url = request.url_for('login_form')
        return RedirectResponse(redirect_url, status_code=302)
    return templates.TemplateResponse('registration.jinja2', context={'request': request})


async def check_username_password(db_user, password):
    return bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8'))


@app.get("/login")
async def login_form(request: Request):
    state_key = None
    return templates.TemplateResponse('login.jinja2', context={'request': request, 'state_key': state_key})


@app.post("/login")
async def login_form(request: Request, response: Response):
    storage = request.app.storage
    data = await request.form()
    username = data.get('username')
    password = data.get('password')
    state_key = data.get('state')
    db_user = await user_utils.get_user_by_username(username=username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")

    if not await check_username_password(db_user, password):
        raise HTTPException(status_code=400, detail="Password is not correct")

    session_id = storage.create_session(username=username, user_id=str(db_user.id))
    state = storage.pop_state(state_key)

    if state:
        pass
    else:
        response.status_code = 200

    response.set_cookie('session_id', session_id)
    return response


@app.get("/logout")
async def logout(request: Request):
    storage = request.app.storage
    session_id = request.cookies.get('session_id')
    storage.remove_session(session_id)
    return {"text": "bye!"}


@app.get('/auth')
@app.post('/auth')
async def auth(request: Request, response: Response):
    storage = request.app.storage
    session_id = request.cookies.get('session_id')
    session = storage.get_session(session_id)
    if not session:
        response.status_code = 401
        return response
    response.status_code = 200
    for h_n, h_v in session.items():
        response.headers[h_n] = h_v
    return response


@app.get("/health")
async def health():
    return {"status": "OK"}


@app.get("/user/profile")
async def profile_form(request: Request):
    storage = request.app.storage
    session_id = request.cookies.get('session_id')
    session = storage.get_session(session_id)
    user_id = session.get('x-user_id')
    db_user = await user_utils.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="user_id not existed")
    return templates.TemplateResponse('profile.jinja2', context={'request': request, 'user': db_user})


@app.post("/user/profile")
async def profile_form(request: Request):
    storage = request.app.storage
    session_id = request.cookies.get('session_id')
    session = storage.get_session(session_id)
    user_id = session.get('x-user_id')
    user = UserUpdate(** await request.form())
    await user_utils.update_user(user_id, user=user)
    redirect_url = request.url_for('profile_form')
    return RedirectResponse(redirect_url, status_code=302)


@app.delete("/user/delete", status_code=204)
async def delete_user(request: Request):
    storage = request.app.storage
    session_id = request.cookies.get('session_id')
    session = storage.get_session(session_id)
    user_id = session.get('x-user_id')
    await user_utils.delete_user(user_id=int(user_id))
