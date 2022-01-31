import asyncio
from db_create import db


async def main():
    await db.set_bind('postgresql://localhost/gino')


# asyncio.set_event_loop(asyncio.new_event_loop())
# asyncio.get_event_loop().run_until_complete(main())
asyncio.run(main())
