"""Routers for my FastApi."""


from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from config import BAD_REQUEST, OK, DEFAULT_ADMIN, KEYS_AUTHOR, CREATED
from json import loads as json_loads
from functions import DBHandler, NotFoundException, \
    BadRequestException, ForbiddenException
from fastapi.exceptions import RequestValidationError


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom exception handler for 400 status code.

    Args:
        request (Request): user request
        exc (RequestValidationError): request exception

    Returns:
        json: exception message
    """
    return JSONResponse(status_code=BAD_REQUEST['code'], content={'detail': BAD_REQUEST})


@app.get("/quote_day", response_class=HTMLResponse)
async def quote_day(request: Request):
    """Method that route get for quote of day page.

    Args:
        request (Request): user request

    Returns:
        _type_: html page
    """
    response = DBHandler.process_day()
    return templates.TemplateResponse("day.html", {"request": request, "quotes": response})


@app.get('/')
async def get_home(request: Request):
    """Method that routes get for main page.

    Args:
        request (Request): user request.

    Returns:
        _type_: html page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/admin')
async def admin(request: Request):
    """Method that routes get for admin page.

    Args:
        request (Request): user request

    Returns:
        _type_: html page
    """
    return templates.TemplateResponse("admin.html", {"request": request, "quotes": DEFAULT_ADMIN})


@app.post('/admin')
async def admin_r(request: Request, token: str = Form(...),\
                  type: str = Form(...), json: str = Form(...)):
    """I don't understand why I did it.

    Args:
        request (Request): user request.
        token (str): user token. Defaults to Form(...).
        json (str): json request. Defaults to Form(...).
        type (str): request type. Defaults to Form(...)

    Returns:
        _type_: html page
    """
    try:
        DBHandler.check_auth(token)
    except ForbiddenException as error:
        return templates.TemplateResponse("admin.html", {"request": request, "quotes": error.detail},
                                          status_code=error.status_code)

    try:
        json = json_loads(json)
    except Exception:
        return templates.TemplateResponse("admin.html", {"request": request, "quotes": BAD_REQUEST},
                                          status_code=BAD_REQUEST['code'])

    if type == 'get':
        try:
            author = str(json['author'])
        except Exception:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": BAD_REQUEST},
                                              status_code=BAD_REQUEST['code'])
        try:
            response = DBHandler.process_get(author)
        except NotFoundException as error:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": error.detail},
                                              status_code=error.status_code)
        except BadRequestException as error:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": error.detail},
                                              status_code=error.status_code)
        return templates.TemplateResponse("quotes.html", {"request": request, "quotes": response})
    if type == 'delete':
        try:
            id = int(json['id'])
        except Exception:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": BAD_REQUEST},
                                              status_code=BAD_REQUEST['code'])
        try:
            response = DBHandler.process_delete(id)
        except NotFoundException as exc:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": exc.detail},
                                              status_code=exc.status_code)
        return templates.TemplateResponse("admin.html", {"request": request, "quotes": response})
    if type == 'post':
        try:
            author = str(json['author'])
        except Exception:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": BAD_REQUEST},
                                              status_code=BAD_REQUEST['code'])
        try:
            body = str(json['body'])
        except Exception:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": BAD_REQUEST},
                                              status_code=BAD_REQUEST['code'])
        try:
            response = DBHandler.process_post(author, body)
        except BadRequestException as err:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": err.detail},
                                              status_code=err.status_code)
        return templates.TemplateResponse("admin.html", {"request": request, "quotes": response})
    if type == 'put':
        try:
            id = int(json['id'])
        except Exception:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": BAD_REQUEST},
                                              status_code=BAD_REQUEST['code'])
        try:
            author = str(json['author'])
        except Exception:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": BAD_REQUEST},
                                              status_code=BAD_REQUEST['code'])
        try:
            body = str(json['body'])
        except Exception:
            return templates.TemplateResponse("admin.html", {"request": request, "quotes": BAD_REQUEST},
                                              status_code=BAD_REQUEST['code'])
        response = DBHandler.process_put(author, body, id)
        return templates.TemplateResponse("admin.html", {"request": request, "quotes": response})


@app.get("/quotes/")
async def postman_get(request: Request, author: str = None, id: int = None):
    """Method that get quote for postman request.

    Args:
        request (Request): user request
        author (str): quote author. Defaults to None.
        id (int): quote id. Defaults to None.

    Raises:
        BadRequestException: raises if author or id invalid

    Returns:
        json: result of work
    """
    DBHandler.check_auth(request.headers.get('Authorization'))
    request_keys = request.query_params.keys()
    for key in request_keys:
        if key not in KEYS_AUTHOR:
            raise BadRequestException
    response = DBHandler.process_get(author, id)
    return JSONResponse(content={'quotes': response}, status_code=OK)


@app.post("/quotes/")
async def postman_post(request: Request, author: str, body: str):
    """Method that post new quote for postman.

    Args:
        request (Request): user request
        author (str): new author
        body (str): new body

    Returns:
        json: result of work
    """
    DBHandler.check_auth(request.headers.get('Authorization'))
    response = DBHandler.process_post(author, body)
    return JSONResponse(content=response, status_code=CREATED)


@app.put("/quotes/")
async def postman_put(request: Request, id: int, author: str, body: str):
    """Method that put new data in quote for postman.

    Args:
        request (Request): user request
        id (int): quote id
        author (str): new author
        body (str): new body

    Returns:
        json: result of work
    """
    DBHandler.check_auth(request.headers.get('Authorization'))
    response = DBHandler.process_put(author, body, id)
    return JSONResponse(content=response, status_code=OK)


@app.delete("/quotes/")
async def postman_delete(request: Request, id: int):
    """Method that delete quote for postman.

    Args:
        request (Request): user request
        id (int): quote id

    Returns:
        json: result of work
    """
    DBHandler.check_auth(request.headers.get('Authorization'))
    response = DBHandler.process_delete(id)
    return JSONResponse(content=response, status_code=OK)


@app.get("/quotes", response_class=HTMLResponse)
async def get_quote(request: Request, author: str = None, id: int = None):
    """Method that routes get from html page.

    Args:
        request (Request): user request
        author (str): quote author. Defaults to None.
        id (int): quote id. Defaults to None.

    Returns:
        _type_: html page.
    """
    if author or id:
        try:
            response = DBHandler.process_get(author, id)
        except NotFoundException as error:
            return templates.TemplateResponse("error.html", {"request": request, "quotes": error.detail})
        return templates.TemplateResponse("quotes.html", {"request": request, "quotes": response})
    response = DBHandler.select_quotes()
    return templates.TemplateResponse("quotes.html", {"request": request, "quotes": response})
