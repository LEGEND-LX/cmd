import asyncio
from collections import deque

from . import *


@bot.on(deadly_cmd(pattern=f"fuck$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"fuck$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 101)
    await eor(event, "fuk")
    animation_chars = ["👉       ✊️", "👉     ✊️", "👉  ✊️", "👉✊️💦"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])
