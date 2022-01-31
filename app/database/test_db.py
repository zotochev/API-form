import asyncio
from gino import Gino


db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.Unicode(), default='noname')


async def main():
    await db.set_bind('postgresql://localhost/gino')
    await db.gino.create_all()

    # further code goes here

    await db.pop_bind().close()


# asyncio.set_event_loop(asyncio.new_event_loop())
# asyncio.get_event_loop().run_until_complete(main())
asyncio.run(main())
#asyncio.get_event_loop().run_until_complete(main())
