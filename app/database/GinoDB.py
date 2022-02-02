import asyncio
from gino import Gino
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from config import ASCEPT_IMGS

import imghdr
import io
from datetime import date
import json


db = Gino()


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


if __name__ == "__main__":
    #asyncio.run(main())

    asyncio.run(insert_user(FILES))
