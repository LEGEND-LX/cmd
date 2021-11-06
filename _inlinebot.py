from math import ceil
from re import compile
import asyncio
import html
import os
import re
import sys
from telethon.events import InlineQuery, callbackquery
from userbot import *
from userbot.cmdhelp import *
from LEGENDBOT.utils import *
import telethon.tl.functions
from userbot.Config import Config
from userbot import ALIVE_NAME
from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
DEFAULTUSER = ALIVE_NAME or "LEGEND"
from . import * 
legend_row = Config.BUTTONS_IN_HELP
legend_emoji1 = Config.EMOJI_IN_HELP1
legend_emoji2 = Config.EMOJI_IN_HELP2
legend_pic = Config.PM_PIC or ""
cstm_pmp = Config.PM_MSG
ALV_PIC = Config.ALIVE_PIC
help_pic = Config.HELP_PIC or "https://telegra.ph/file/6a08bc3d83b51923f47b2.jpg"
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Config.LOGGER_ID
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
)

USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**🚫 Blocked and Reported**"

LEGEND_FIRST = (
    "𝙷𝚎𝚕𝚕𝚘 𝚂𝚒𝚛/𝙼𝚒𝚜𝚜,\n𝙸 𝚑𝚊𝚟𝚎𝚗'𝚝 𝚊𝚙𝚙𝚛𝚘𝚟𝚎𝚍 𝚢𝚘𝚞 𝚢𝚎𝚝 𝚝𝚘 𝚙𝚎𝚛𝚜𝚘𝚗𝚊𝚕 𝚖𝚎𝚜𝚜𝚊𝚐𝚎 𝚖𝚎😎⚠️.\n"
    "𝐓𝐡𝐢𝐬 𝐈𝐬 𝐌𝐲 𝐎𝐰𝐧𝐞𝐫 {}\n\n"
    "**{}**\n\nPlease Choose Why u Are Here♥️!!"
)

alive_txt = """
    **{}**\n
   **♥️ẞø† ẞ†α†µѕ♥️**
**•⚜️•Øաղ̃ҽ̈r :** {}\n
**•🌹•Lêɠêɳ̃dẞø† :** {}
**•🌹•†ҽ̀lҽ́ƭhøղ  :** {}
**•🌹•Ãbûßê     :** {}
**•🌹•ßudø      :** {}
**•🌹•Bø†       :** {}
"""

def button(page, modules):
    Row = legend_row
    Column = 3

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(f"{legend_emoji1} " + pair + f" {legend_emoji2}", data=f"Information[{page}]({pair})")
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
               f"⭅ϐαϲκ", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"♦️ ❎ ♦️", data="close"
            ),
            custom.Button.inline(
               f"ղҽxԵ⭆", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]


    modules = CMD_HELP
if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query == "legendbot_help":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            help_msg = f"𓆩♥️{legend_mention}♥️𓆪\n\n**🕹️𝚃𝚘𝚝𝚊𝚕 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚍⭆ `{len(CMD_HELP)}`**\n**⌨️Tοταℓ Cοммαи∂ѕ⭆ `{len(apn)}`**\n**🎒Pαցҽ⭆ 1/{veriler[0]}** \n"
            if help_pic and help_pic.endswith((".jpg", ".png")):
                result = builder.photo(
                    help_pic,
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic:
                result = builder.document(
                    help_pic,
                    text=help_msg,
                    title="LegendBot Alive",
                    buttons=veriler[1],
                    link_preview=False,
                )
            else:
                result = builder.article(
                    f"Hey! Only use .op please",
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
        elif event.query.user_id == bot.uid and query.startswith("fsub"):
            hunter = event.pattern_match.group(1)
            legend = hunter.split("+")
            user = await bot.get_entity(int(legend[0]))
            channel = await bot.get_entity(int(legend[1]))
            msg = f"**👋 Welcome** [{user.first_name}](tg://user?id={user.id}), \n\n**📍 You need to Join** {channel.title} **to chat in this group.**"
            if not channel.username:
                link = (await bot(ExportChatInviteRequest(channel))).link
            else:
                link = "https://t.me/" + channel.username
            result = [
                await builder.article(
                    title="force_sub",
                    text = msg,
                    buttons=[
                        [Button.url(text="Channel", url=link)],
                        [custom.Button.inline("🔓 Unmute Me", data=unmute)],
                    ],
                )
            ]
 
        elif event.query.user_id == bot.uid and query == "alive":
            leg_end = alive_txt.format(Config.ALIVE_MSG, legend_mention, LEGENDversion, version.__version__, abuse_m, is_sudo, Config.BOY_OR_GIRL)
            alv_btn = [
                [Button.url(f"{LEGEND_USER}", f"tg://openmessage?user_id={Its_LegendBoy}")],
                [Button.url("My Channel", f"https://t.me/{my_channel}"), 
                Button.url("My Group", f"https://t.me/{my_group}")],
            ]
            if ALV_PIC and ALV_PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    ALV_PIC,
                    text=leg_end,
                    buttons=alv_btn,
                    link_preview=False,
                )
            elif ALV_PIC:
                result = builder.document(
                    ALV_PIC,
                    text=leg_end,
                    title="LegendBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=leg_end,
                    title="LegendBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                )

        elif event.query.user_id == bot.uid and query == "pm_warn":
            lege_nd = LEGEND_FIRST.format(legend_mention, mssge)
            result = builder.photo(
                file=legend_pic,
                text=lege_nd,
                buttons=[
                    [
                        custom.Button.inline("📝 Request 📝", data="req"),
                        custom.Button.inline("💬 Chat 💬", data="chat"),
                    ],
                    [custom.Button.inline("🚫 Spam 🚫", data="heheboi")],
                    [custom.Button.inline("Curious ❓", data="pmclick")],
                ],
            )

        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**⚜ 𝙻𝚎𝚐𝚎𝚗𝚍𝚊𝚛𝚢 𝙰𝚏 𝙻𝚎𝚐𝚎𝚗𝚍𝙱𝚘𝚝 ⚜**",
                buttons=[
                    [Button.url("♥️ 𝚁𝚎𝚙𝚘 ♥", "https://github.com/LEGEND-OS/LEGENDBOT")],
                    [Button.url("♦️ Deploy ♦️", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FLEGEND-OS%2FLEGENDBOT&template=https%3A%2F%2Fgithub.com%2FLEGEND-OS%2FLEGENDBOT")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[‏‏‎ ‎]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@Legend_Userbot",
                text="""**Hey! This is [Lêɠêɳ̃dẞø†](https://t.me/its_LegendBot) \nYou can know more about me from the links given below 👇**""",
                buttons=[
                    [
                        custom.Button.url("🔥 CHANNEL 🔥", "https://t.me/Its_LegendBot"),
                        custom.Button.url(
                            "⚡ GROUP ⚡", "https://t.me/Legend_Userbot"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "✨ REPO ✨", "https://github.com/LEGEND-OS/LEGENDBOT"),
                        custom.Button.url
                    (
                            "🔰 TUTORIAL 🔰", "https://youtu.be/bPzvmaQejNM"
                    )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for Other Users..."
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"🔰 This is Lêɠêɳ̃dẞø† PM Security for {legend_mention} to keep away unwanted retards from spamming PM..."
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"✅ **Request Registered** \n\n{legend_mention} will now decide to look for your request or not.\n😐 Till then wait patiently and don't spam!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**👀 Hey {legend_mention} !!** \n\n⚜️ You Got A Request From [{first_name}](tg://user?id={ok}) In PM!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"chat")))
    async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Ahh!! You here to do chit-chat!!\n\nPlease wait for {legend_mention} to come. Till then keep patience and don't spam."
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**👀 Hey {legend_mention} !!** \n\n⚜️ You Got A PM from  [{first_name}](tg://user?id={ok})  for random chats!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"🥴 **Nikal lawde\nPehli fursat me nikal**"
            )
            await event.client(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await bot.send_message(
                LOG_GP,
                f"**Blocked**  [{first_name}](tg://user?id={ok}) \n\nReason:- Spam",
            )


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"unmute")))
    async def on_pm_click(event):
        hunter = (event.data_match.group(1)).decode("UTF-8")
        legend = hunter.split("+")
        if not event.sender_id == int(legend[0]):
            return await event.answer("This Ain't For You!!", alert=True)
        try:
            await bot(GetParticipantRequest(int(legend[1]), int(legend[0])))
        except UserNotParticipantError:
            return await event.answer(
                "You need to join the channel first.", alert=True
            )
        await bot.edit_permissions(
            event.chat_id, int(legend[0]), send_message=True, until_date=None
        )
        await event.edit("Yay! You can chat now !!")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
            if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
                current_page_number=0
                simp = button(current_page_number, CMD_HELP)
                veriler = button(0, sorted(CMD_HELP))
                apn = []
                for x in CMD_LIST.values():
                    for y in x:
                        apn.append(y)
                await event.edit(
                    f"",
                    buttons=simp[1],
                    link_preview=False,
                )
            else:
                reply_pop_up_alert = "οн ϲοммοи γαяя υ τнιиκ υ ϲαи ϲℓιϲκ οи ιτ😁😁😁. ∂єρℓογ υя οωи ϐοτ. © Lêɠêɳ̃dẞø†™"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            veriler = custom.Button.inline(f"{legend_emoji1} Re-Open Menu {legend_emoji2}", data="reopen")
            await event.edit(f"**⚜️ Lêɠêɳ̃dẞø† Mêñû Prõvîdêr háš běěn čłøšĕd by {legend_mention} ⚜️**\n\n**Bot Of :**  {legend_mention}\n\n            [©️Lêɠêɳ̃dẞø†]({chnl_link})", buttons=veriler, link_preview=False)
        else:
            reply_pop_up_alert = "κγα υиgℓι καя янє нο мєяє ϐοτ ραя αgαя ϲнαнιγє τοн κнυ∂ κα ϐαиα ℓο иα. Aα נατє нο υиgℓι καяиє мєяє ϐοτ ρє.   ©Lêɠêɳ̃dẞø†"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
   

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f"**𓆩♥️{legend_mention}♥️𓆪**\n\n**🕹️𝚃𝚘𝚝𝚊𝚕 𝙼𝚘𝚍𝚞𝚕𝚎𝚜 𝙸𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚍⭆ `{len(CMD_HELP)}`**\n**⌨️𝚃𝚘𝚝𝚊𝚕 𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜⭆ `{len(apn)}`**\n**🎒𝙿𝚊𝚐𝚎⭆ {page + 1}/{veriler[0]}**",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "κγα υиgℓι καя янє нο мєяє ϐοτ ραя αgαя ϲнαнιγє τοн κнυ∂ κα ϐαиα ℓο иα αα נατє нο υиgℓι καяиє мєяє ϐοτ ρє.   ©Lêɠêɳ̃dẞø†",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "♦️ " + cmd[0] + " ♦️", data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "No Description is written for this plugin", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{legend_emoji1} Main Menu {legend_emoji2}", data=f"page({page})")])
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f"**📗 𝙵𝚒𝚕𝚎 :**  `{commands}`\n**🔢 Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. ©Lêɠêɳ̃dẞø†™",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**📗 𝙵𝚒𝚕𝚎 :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ 𝚆𝚊𝚛𝚗𝚒𝚗𝚐 :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ 𝚆𝚊𝚛𝚗𝚒𝚗𝚐 :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**⚡ Type :**  {CMD_HELP_BOT[cmd]['info']['type']}\n"
            result += f"**ℹ️ 𝙸𝚗𝚏𝚘 :**  {CMD_HELP_BOT[cmd]['info']['info']}\n\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**🛠 𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜 :**  `{COMMAND_HAND_LER[:1]}{command['command']}`\n"
        else:
            result += f"**🛠 𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜 :**  `{COMMAND_HAND_LER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**💬 𝙴𝚡𝚙𝚕𝚊𝚗𝚊𝚝𝚒𝚘𝚗 :**  `{command['usage']}`\n\n"
        else:
            result += f"**💬 𝙴𝚡𝚙𝚕𝚊𝚗𝚊𝚝𝚒𝚘𝚗 :**  `{command['usage']}`\n"
            result += f"**⌨️ 𝙵𝚘𝚛 𝙴𝚡𝚊𝚖𝚙𝚕𝚎 :**  `{COMMAND_HAND_LER[:1]}{command['example']}`\n\n"
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                result,
                buttons=[
                    custom.Button.inline(f"{legend_emoji1} Return {legend_emoji2}", data=f"Information[{page}]({cmd})")
                ],
                link_preview=False,
            )
        else:
            return await event.answer(
                "ᵃᵇʰⁱ ᵗᵃᵏ ⁿʰⁱ ˢᵃᵐʲʰᵃ ᵏʰᵘᵈᵏᵃ ᵇᵃⁿᵃ ˡᵒ ⁿᵃ ᵗᵒʰ ᵘˢᵉ ᵏᵃʳⁿᵃ ʰ ᵗᵒʰ ᵏʸᵃ ᵘⁿᵍˡⁱ ᵏᵃʳ ʳʰᵉ ʰᵒ.🤦‍♂️🤦‍♂️🤦‍♂️ ©Lêɠêɳ̃dẞø†™ ",
                cache_time=0,
                alert=True,
            )





    
