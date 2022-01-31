from sanic import Sanic
from sanic.response import text
from database.FakeDB import db
import json


app = Sanic("MyHelloWorldApp")


@app.get("/")
async def hello_world(request):
    result = "Collected forms\n"
    result += "---------\n"
    result += "\n".join([str(x) for x in db.forms])
    result += "\n---------"
    return text(result)


@app.post("/api/form")
async def hello_world(request):
    print('recieved request')
    print('HEAD')
    print(request.head)
    #print('BODY')
    #print(request.body)
    print('FILE')
    #print(request.files)
#    print(type(request.files.get('file').body))
#    with open('outfile.jpg', 'wb') as outfile:
#        outfile.write(request.files.get('file').body)
    test = json.loads(request.files.get('form_my').body.decode('utf8'))
    print(type(test))
    print(test)

    #print(f'{str(request.json)}')
    #db.insert(request.json)
    return text('{xxxxxx}')
