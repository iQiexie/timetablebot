# import asyncio
# import glob
# from pathlib import Path
#
# from app.Database import Database
# from app.backend.base.db import async_session
# from app.backend.users.crud import UserCRUD
#
# path = Path(r"D:\Desktop\PycharmProjects\TimeTableBot\app\DATABASE\USERS")
# users_raw = [str(pp) for pp in path.glob("*.db")]
# users = []
#
#
# async def run():
#     for user in users_raw:
#         user = user.split("""D:\\Desktop\\PycharmProjects\\TimeTableBot\\app\\DATABASE\\USERS\\""")[1]
#         user_id = user.split('.')[0]
#
#         db = Database(user_id)
#         group = db.get_group_index()
#
#         db = UserCRUD(async_session)
#         await db.create(
#             vk_id=int(user_id),
#             group_index=int(group)
#         )
#
# asyncio.run(run())
#
#
