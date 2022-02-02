from sanic import Sanic, response
from sanic.response import text
from database.GinoDB import db, Forms, Users, insert_user
import json

import base64


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def get_base64_encoded_image_bytes(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')



app = Sanic("MyHelloWorldApp")


@app.listener("after_server_start")
async def setup_db(app, loop):
    await db.set_bind('postgresql://gino:9827357@127.0.0.1/gino')
    await db.gino.create_all()
    app.ctx.db = db


@app.listener("before_server_stop")
async def unsetup_db(app, loop):
    app.ctx.db.pop_bind().close()


def create_table():
    def insert_line():
        line = ''
        line += '<tr>'
        for item in items:
            line += '<th>'
            line += 'item'
            line += '</th>'
        line += '</tr>'
        return line

    result = ''
    result += '<table>'
    for line in lines:
        insert_line()
    result += '</table>'


@app.get("/")
async def hello_world(request):
    result = ''
    result += "<p>Collected forms</p>\n"
    result += "<p>---------</p>\n"

    all_users = await Users.query.gino.all()
    # print([(x.id, x.name) for x in all_users])

    result += "\n".join(['<p>-' + str((x.id, x.name)) + f'<img src="data:image/jpeg;base64,{get_base64_encoded_image_bytes(x.image)}">''+ </p>' for x in all_users])
    result += "\n<p>---------</p>"

    bs64 = get_base64_encoded_image('test_pic.jpeg')
    result += f'<img src="data:image/jpeg;base64,{bs64}">'
    #result += f'<img src="data:image/jpeg;base64,{get_base64_encoded_image_bytes(x.image)}">'
    return response.html(result)


@app.post("/api/form")
async def hello_world(request):
    with open('outfile.jpg', 'wb') as outfile:
        outfile.write(request.files.get('file').body)
    test = json.loads(request.files.get('form').body.decode('utf8'))

    request_json = dict()
    request_json['file'] = request.files.get('file').body
    request_json['form'] = json.loads(request.files.get('form').body.decode('utf8'))

    await insert_user(request_json)
    print(type(test))
    print(test)


    #db.insert(request.json)
    # return то что отправляется автору запроса
    return text('{xxxxxx}')
