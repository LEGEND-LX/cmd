from userbot.Config import Config
import asyncio

import requests
from telethon import functions
from . import *
from userbot import ALIVE_NAME, CMD_LIST, SUDO_LIST
from LEGENDBOT.utils import admin_cmd, edit_or_reply, sudo_cmd

perf = "[ †hê Lêɠêɳ̃dẞø† ]"

import requests
from telethon import functions
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot, BotInlineDisabledError as noinline, YouBlockedUserError


msg = f"""
**⚜ 𝙻𝚎𝚐𝚎𝚗𝚍𝚊𝚛𝚢 𝙰𝚏 𝙻𝚎𝚐𝚎𝚗𝚍𝙱𝚘𝚝 ⚜**

  •        [♥️ 𝚁𝚎𝚙𝚘 ♥️](https://github.com/LEGEND-OS/LEGENDBOT)
  •        [♦️ Deploy ♦️](https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FLEGEND-OS%2FLEGENDBOT&template=https%3A%2F%2Fgithub.com%2FLEGEND-OS%2FLEGENDBOT)

  •  ©️ {Legend_channel} ™
"""
botname = Config.BOT_USERNAME

@bot.on(admin_cmd(pattern="repo$"))
@bot.on(sudo_cmd(pattern="repo$", allow_sudo=True))
async def repo(event):
    try:
        legend = await bot.inline_query(botname, "repo")
        await legend[0].click(event.chat_id)
        if event.sender_id == Its_LegendBoy:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


@bot.on(admin_cmd(pattern="op ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="op ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "legendbot_help")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except noinline:
            legend = await eor(event, "**Inline Mode is disabled.** \n__Turning it on, please wait for a minute...__")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message(perf)
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await legend.edit("Unblock @Botfather first.")
                await legend.edit(f"**Turned On Inline Mode Successfully.** \n\nDo `{l1}op` again to get the help menu.")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await eor(event, "**⚠️ 𝙴𝚁𝚁𝙾𝚁 !!** \n𝙿𝚕𝚎𝚊𝚜𝚎 𝚁𝚎-𝙲𝚑𝚎𝚌𝚔 BOT_TOKEN & BOT_USERNAME on Heroku.")


@bot.on(admin_cmd(pattern="plinfo(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="plinfo(?: |$)(.*)", allow_sudo=True))
async def legendbott(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await eor(event, str(CMD_HELP[args]))
        else:
            await eor(event, "**⚠️ 𝙴𝚛𝚛𝚘𝚛 !** \n𝙽𝚎𝚎𝚍 𝚊 Plugin 𝚗𝚊𝚖𝚎 𝚝𝚘 𝚜𝚑𝚘𝚠 𝚙𝚕𝚞𝚐𝚒𝚗 𝚒𝚗𝚏𝚘")
    else:
        string = ""
        sayfa = [
            sorted(list(CMD_HELP))[i : i + 5]
            for i in range(0, len(sorted(list(CMD_HELP))), 5)
        ]

        for i in sayfa:
            string += f"`♦️`"
            for sira, a in enumerate(i):
                string += "`" + str(a)
                if sira == i.index(i[-1]):
                    string += "`"
                else:
                    string += "`, "
            string += "\n"
        await eor(event, "Please Specify A Module Name Of Which You Want Info" + "\n\n" + string)
