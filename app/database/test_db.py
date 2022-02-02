import asyncio
from gino import Gino
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.Unicode(), default='noname')


async def main():
    
    await db.set_bind('postgresql://gino:9827357@127.0.0.1/gino')
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


class Test:
    text = 'Hello'

    async def some_method(self):
        await asyncio.sleep(0.1)
        print(self.text)


async def test_main():
    test = Test('Hello')

    await test.some_method()


if __name__ == "__main__":
    # asyncio.set_event_loop(asyncio.new_event_loop())
    # asyncio.get_event_loop().run_until_complete(main())
    # asyncio.run(main())
    # asyncio.get_event_loop().run_until_complete(main())

    asyncio.run(test_main())
