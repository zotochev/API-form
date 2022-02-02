from sanic import Sanic, response
from sanic.response import text, HTTPResponse
import json
import base64

from database.GinoDB import db, Forms, Users, insert_user
from config import API_POST_FORMS, DB_URL, SERVER_NAME


def get_base64_encoded_image_bytes(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')


app = Sanic(SERVER_NAME)


@app.listener("after_server_start")
async def setup_db(app, loop):
    await db.set_bind(DB_URL)
    await db.gino.create_all()
    app.ctx.db = db


@app.listener("before_server_stop")
async def unsetup_db(app, loop):
    app.ctx.db.pop_bind().close()


@app.get("/")
async def hello_world(request):
    result = ''
    result += "<p>Collected forms</p>\n"
    result += "<p>---------</p>\n"

    all_users = await Users.query.gino.all()
    # print([(x.id, x.name) for x in all_users])

    result += "\n".join(['<p>-' + str((x.id, x.name)) + f'<img src="data:image/jpeg;base64,{get_base64_encoded_image_bytes(x.image)}" height="30">''+ </p>' for x in all_users])
    result += "\n<p>---------</p>"

    return response.html(result)


@app.post(API_POST_FORMS)
async def post_form(request):

    try:
        await insert_user(request)
    except KeyError as ke:
        return HTTPResponse(body='{'f"'KeyError': {ke}"'}', status=400)
    except TypeError as te:
        return HTTPResponse(body='{'f"'TypeError': {te}"'}', status=400)
    except Exception as e:
        return HTTPResponse(body='{'f"ServerError: {e}"'}', status=500)

    return HTTPResponse(status=200)
