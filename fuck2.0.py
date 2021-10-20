type .moj and .bete to see the fun.
"""
import random, re
from uniborg.util import admin_cmd
import asyncio
from telethon import events

@borg.on(admin_cmd(pattern="moj?(.*)"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("RE")
        await asyncio.sleep(0.7)
        await event.edit("BHSDK")
        await asyncio.sleep(1)
        await event.edit("BETE")
        await asyncio.sleep(0.8)
        await event.edit("MOJ ")
        await asyncio.sleep(0.9)
        await event.edit("KRDI")
        await asyncio.sleep(1)
        await event.edit("TUM TO")
        await asyncio.sleep(0.8)
        await event.edit("😈")
        await asyncio.sleep(0.7)
        await event.edit("BADE HEAVY DRIVER HO BETE")
        await asyncio.sleep(1)
        await event.edit("😂RE BHSDK BETE MOJ KRDI TUM TO BADE HEAVY DRIVER HO🤣 ")

@borg.on(events.NewMessage(pattern=r"\.nehi", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("bhsdk beteeeeeeesssesseeeee ma chuda")
    await asyncio.sleep(999)
