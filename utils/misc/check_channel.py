from typing import Union
from loader import bot


async def check(user_id, channel: Union[int, str]):
    member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    return member.is_chat_member()


