from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse
from config import *
import uvicorn
import requests
from database import fill_database, get_from_db, update_db, delete_from_db
from pydantic import BaseModel
from checker import check_auth


class Media(BaseModel):
    id: int
    siteUrl: str
    title: dict
    description: str

    def to_dict(self):
        return self.__dict__


app = FastAPI()
env = Environment(loader=FileSystemLoader('templates'), autoescape=True)


@app.get("/")
async def root():
    template = env.get_template('home.html')
    content = template.render()
    return HTMLResponse(content=content)


@app.get("/media_api")
async def media_api():
    response = requests.post(URL, json={'query': QUERY})
    data = response.json()['data']['Page']['media']
    template = env.get_template('index.html')
    content = template.render(data=data)
    return HTMLResponse(content=content)


@app.get("/media_api/{index}")
async def media_api_pages(index: int):
    response = requests.post(URL, json={'query': QUERY})
    data = response.json()['data']['Page']['media']
    template = env.get_template('media.html')
    content = template.render(data=data[index - 1])
    return HTMLResponse(content=content)


@app.get("/media")
async def media():
    data = get_from_db(CLIENT)
    template = env.get_template('my_index.html')
    content = template.render(data=data)
    return HTMLResponse(content=content)


@app.get("/media/{index}")
async def media_pages(index: int):
    data = get_from_db(CLIENT)
    template = env.get_template('media.html')
    content = template.render(data=data[index - 1])
    return HTMLResponse(content=content)


@app.post("/media")
async def create_media(title: Media | None = None, auth: str = None):
    check_auth(auth)
    fill_database(CLIENT, title.to_dict())
    return MESSAGE.format('created')


@app.put("/media")
async def update_media(title: Media | None = None, auth: str = None):
    check_auth(auth)
    update_db(CLIENT, title.to_dict()['id'], title.to_dict())
    return MESSAGE.format('updated')


@app.delete("/media")
async def delete_media(title: Media | None = None, auth: str = None):
    check_auth(auth)
    delete_from_db(CLIENT, title.to_dict()['id'])
    return MESSAGE.format('deleted')

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=APP_PORT)
