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

USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**๐ซ Blocked and Reported**"

LEGEND_FIRST = (
    "๐ท๐๐๐๐ ๐๐๐/๐ผ๐๐๐,\n๐ธ ๐๐๐๐๐'๐ ๐๐๐๐๐๐๐๐ ๐ข๐๐ ๐ข๐๐ ๐๐ ๐๐๐๐๐๐๐๐ ๐๐๐๐๐๐๐ ๐๐๐โ ๏ธ.\n"
    "๐๐ก๐ข๐ฌ ๐๐ฌ ๐๐ฒ ๐๐ฐ๐ง๐๐ซ {}\n\n"
    "**{}**\n\nPlease Choose Why u Are Hereโฅ๏ธ!!"
)

alive_txt = """
    **{}**\n
   **โฅ๏ธแบรธโ  แบโ ฮฑโ ยตัโฅ๏ธ**
**โขโ๏ธโขรีกีฒฬาฝฬr :** {}\n
**โข๐นโขLรชษ รชษณฬdแบรธโ  :** {}
**โข๐นโขโ าฝฬlาฝฬฦญhรธีฒ  :** {}
**โข๐นโขรbรปรรช     :** {}
**โข๐นโขรudรธ      :** {}
**โข๐นโขBรธโ        :** {}
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
               f"โญฯฮฑฯฒฮบ", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"โฆ๏ธ โ โฆ๏ธ", data="close"
            ),
            custom.Button.inline(
               f"ีฒาฝxิตโญ", data=f"page({0 if page == (max_pages - 1) else page + 1})"
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
            help_msg = f"๐ฉโฅ๏ธ{legend_mention}โฅ๏ธ๐ช\n\n**๐น๏ธ๐๐๐๐๐ ๐ผ๐๐๐๐๐๐ ๐ธ๐๐๐๐๐๐๐๐โญ `{len(CMD_HELP)}`**\n**โจ๏ธTฮฟฯฮฑโ Cฮฟะผะผฮฑะธโัโญ `{len(apn)}`**\n**๐Pฮฑึาฝโญ 1/{veriler[0]}** \n"
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
            msg = f"**๐ Welcome** [{user.first_name}](tg://user?id={user.id}), \n\n**๐ You need to Join** {channel.title} **to chat in this group.**"
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
                        [custom.Button.inline("๐ Unmute Me", data=unmute)],
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
                        custom.Button.inline("๐ Request ๐", data="req"),
                        custom.Button.inline("๐ฌ Chat ๐ฌ", data="chat"),
                    ],
                    [custom.Button.inline("๐ซ Spam ๐ซ", data="heheboi")],
                    [custom.Button.inline("Curious โ", data="pmclick")],
                ],
            )

        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**โ ๐ป๐๐๐๐๐๐๐๐ข ๐ฐ๐ ๐ป๐๐๐๐๐๐ฑ๐๐ โ**",
                buttons=[
                    [Button.url("โฅ๏ธ ๐๐๐๐ โฅ", "https://github.com/LEGEND-OS/LEGENDBOT")],
                    [Button.url("โฆ๏ธ Deploy โฆ๏ธ", "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FLEGEND-OS%2FLEGENDBOT&template=https%3A%2F%2Fgithub.com%2FLEGEND-OS%2FLEGENDBOT")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[โโโ โ]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@Legend_Userbot",
                text="""**Hey! This is [Lรชษ รชษณฬdแบรธโ ](https://t.me/its_LegendBot) \nYou can know more about me from the links given below ๐**""",
                buttons=[
                    [
                        custom.Button.url("๐ฅ CHANNEL ๐ฅ", "https://t.me/Its_LegendBot"),
                        custom.Button.url(
                            "โก GROUP โก", "https://t.me/Legend_Userbot"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "โจ REPO โจ", "https://github.com/LEGEND-OS/LEGENDBOT"),
                        custom.Button.url
                    (
                            "๐ฐ TUTORIAL ๐ฐ", "https://youtu.be/bPzvmaQejNM"
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
                f"๐ฐ This is Lรชษ รชษณฬdแบรธโ  PM Security for {legend_mention} to keep away unwanted retards from spamming PM..."
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"โ **Request Registered** \n\n{legend_mention} will now decide to look for your request or not.\n๐ Till then wait patiently and don't spam!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**๐ Hey {legend_mention} !!** \n\nโ๏ธ You Got A Request From [{first_name}](tg://user?id={ok}) In PM!!"
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
            tosend = f"**๐ Hey {legend_mention} !!** \n\nโ๏ธ You Got A PM from  [{first_name}](tg://user?id={ok})  for random chats!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"๐ฅด **Nikal lawde\nPehli fursat me nikal**"
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
                reply_pop_up_alert = "ฮฟะฝ ฯฒฮฟะผะผฮฟะธ ฮณฮฑัั ฯ ฯะฝฮนะธฮบ ฯ ฯฒฮฑะธ ฯฒโฮนฯฒฮบ ฮฟะธ ฮนฯ๐๐๐. โัฯโฮฟฮณ ฯั ฮฟฯะธ ฯฮฟฯ. ยฉ Lรชษ รชษณฬdแบรธโ โข"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            veriler = custom.Button.inline(f"{legend_emoji1} Re-Open Menu {legend_emoji2}", data="reopen")
            await event.edit(f"**โ๏ธ Lรชษ รชษณฬdแบรธโ  Mรชรฑรป Prรตvรฎdรชr hรกลก bฤฤn ฤลรธลกฤd by {legend_mention} โ๏ธ**\n\n**Bot Of :**  {legend_mention}\n\n            [ยฉ๏ธLรชษ รชษณฬdแบรธโ ]({chnl_link})", buttons=veriler, link_preview=False)
        else:
            reply_pop_up_alert = "ฮบฮณฮฑ ฯะธgโฮน ฮบฮฑั ัะฝั ะฝฮฟ ะผััั ฯฮฟฯ ฯฮฑั ฮฑgฮฑั ฯฒะฝฮฑะฝฮนฮณั ฯฮฟะฝ ฮบะฝฯโ ฮบฮฑ ฯฮฑะธฮฑ โฮฟ ะธฮฑ. Aฮฑ ื ฮฑฯั ะฝฮฟ ฯะธgโฮน ฮบฮฑัะธั ะผััั ฯฮฟฯ ฯั.   ยฉLรชษ รชษณฬdแบรธโ "
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
                f"**๐ฉโฅ๏ธ{legend_mention}โฅ๏ธ๐ช**\n\n**๐น๏ธ๐๐๐๐๐ ๐ผ๐๐๐๐๐๐ ๐ธ๐๐๐๐๐๐๐๐โญ `{len(CMD_HELP)}`**\n**โจ๏ธ๐๐๐๐๐ ๐ฒ๐๐๐๐๐๐๐โญ `{len(apn)}`**\n**๐๐ฟ๐๐๐โญ {page + 1}/{veriler[0]}**",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "ฮบฮณฮฑ ฯะธgโฮน ฮบฮฑั ัะฝั ะฝฮฟ ะผััั ฯฮฟฯ ฯฮฑั ฮฑgฮฑั ฯฒะฝฮฑะฝฮนฮณั ฯฮฟะฝ ฮบะฝฯโ ฮบฮฑ ฯฮฑะธฮฑ โฮฟ ะธฮฑ ฮฑฮฑ ื ฮฑฯั ะฝฮฟ ฯะธgโฮน ฮบฮฑัะธั ะผััั ฯฮฟฯ ฯั.   ยฉLรชษ รชษณฬdแบรธโ ",
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
                    "โฆ๏ธ " + cmd[0] + " โฆ๏ธ", data=f"commands[{commands}[{page}]]({cmd[0]})"
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
                f"**๐ ๐ต๐๐๐ :**  `{commands}`\n**๐ข Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. ยฉLรชษ รชษณฬdแบรธโ โข",
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
        result = f"**๐ ๐ต๐๐๐ :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**โ ๏ธ ๐๐๐๐๐๐๐ :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**โ ๏ธ ๐๐๐๐๐๐๐ :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**โก Type :**  {CMD_HELP_BOT[cmd]['info']['type']}\n"
            result += f"**โน๏ธ ๐ธ๐๐๐ :**  {CMD_HELP_BOT[cmd]['info']['info']}\n\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**๐  ๐ฒ๐๐๐๐๐๐๐ :**  `{COMMAND_HAND_LER[:1]}{command['command']}`\n"
        else:
            result += f"**๐  ๐ฒ๐๐๐๐๐๐๐ :**  `{COMMAND_HAND_LER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**๐ฌ ๐ด๐ก๐๐๐๐๐๐๐๐๐ :**  `{command['usage']}`\n\n"
        else:
            result += f"**๐ฌ ๐ด๐ก๐๐๐๐๐๐๐๐๐ :**  `{command['usage']}`\n"
            result += f"**โจ๏ธ ๐ต๐๐ ๐ด๐ก๐๐๐๐๐ :**  `{COMMAND_HAND_LER[:1]}{command['example']}`\n\n"
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
                "แตแตสฐโฑ แตแตแต โฟสฐโฑ หขแตแตสฒสฐแต แตสฐแตแตแตแต แตแตโฟแต หกแต โฟแต แตแตสฐ แตหขแต แตแตสณโฟแต สฐ แตแตสฐ แตสธแต แตโฟแตหกโฑ แตแตสณ สณสฐแต สฐแต.๐คฆโโ๏ธ๐คฆโโ๏ธ๐คฆโโ๏ธ ยฉLรชษ รชษณฬdแบรธโ โข ",
                cache_time=0,
                alert=True,
            )





    
