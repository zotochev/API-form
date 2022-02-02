import asyncio
from gino import Gino
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from config import ASCEPT_IMGS

import imghdr
import io
from datetime import date
import json


db = Gino()

QUIZ = {
            'first': "1Hello",
            'second': "2World",
            'third': "3World",
            'fourth': "4World",
            'fifth': "5World",
        }

FORM = {
            "name": "John Doe",
            "gender": "1",
            "birth_day": "1990-04-07",
            "quiz": QUIZ,
        }

FILE_NAME = "test_pic.jpeg"
URL = 'http://localhost:8000/api/form'

FILES = {
            'form': json.dumps(FORM),
            'file': open(FILE_NAME, 'rb'),
        }


class Users(db.Model):
    __tablename__ = 'users_info'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(), default='no name')
    gender = db.Column(db.Boolean())
    birth_day = db.Column(db.Date())
    image = db.Column(db.LargeBinary())


class Forms(db.Model):
    __tablename__ = 'forms'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    first = db.Column(db.Unicode())
    second = db.Column(db.Unicode())
    third = db.Column(db.Unicode())
    fourth = db.Column(db.Unicode())
    fifth = db.Column(db.Unicode())


async def insert_user(api_input: dict):
    def prepare_input(api_input):
        request_json = dict()

        request_json['file'] = api_input.files.get('file').body
        # check if file is image
        file = io.BytesIO(request_json['file'])
        if imghdr.what(file).lower() not in ASCEPT_IMGS:
            raise TypeError(f"Wrong file type: {api_input.files.get('file').type}")

        request_json['form'] = json.loads(api_input.files.get('form').body.decode('utf8'))
        return request_json

    api_input = prepare_input(api_input)

    # TABLE users 
    users_name = api_input['form']['name']
    users_gender = bool(int(api_input['form']['gender']))
    users_birth_day = date.fromisoformat(api_input['form']['birth_day'])
    users_file = api_input['file']

    user = await Users.create(
                name=users_name,
                gender=users_gender,
                birth_day=users_birth_day,
                image=users_file, 
            )

    # TABLE forms
    forms_first = api_input['form']['quiz']['first']
    forms_secon = api_input['form']['quiz']['second']
    forms_third = api_input['form']['quiz']['third']
    forms_fourth = api_input['form']['quiz']['fourth']
    forms_fifth = api_input['form']['quiz']['fifth']

    form = await Forms.create(
                user_id=user.id,
                first=forms_first,
                second=forms_secon,
                third=forms_third,
                fourth=forms_fourth,
                fifth=forms_fifth,
            )


async def main():

    await db.set_bind('postgresql://gino:9827357@127.0.0.1/gino')
    # Что за команда?
    await db.gino.create_all()

    # create a new user
    user = await User.create(nickname='fantix')
    # get its name
    name = await User.select('nickname').where(
        User.id == user.id).gino.scalar()

    assert name == user.nickname  # they are both 'fantix' before the update
    # modification here
    await user.update(nickname='daisy').apply()
    # SQL (parameters: 'daisy', 1):
    # UPDATE users SET nickname=$1 WHERE users.id = $2 RETURNING users.nickname
    print(user.nickname)  # daisy

    # get its name again
    name = await User.select('nickname').where(
        User.id == user.id).gino.scalar()
    print(name)  # daisy
    assert name == user.nickname  # they are both 'daisy' after the update

    all_users = await User.query.gino.all()
    print([x.nickname for x in all_users])

    await db.pop_bind().close()


async def main_test():
    test = DBHandler(db)




if __name__ == "__main__":
    #asyncio.run(main())

    asyncio.run(insert_user(FILES))
