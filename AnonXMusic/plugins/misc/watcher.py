import os
import re
import time

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.utils.database import is_afk, remove_afk
from AnonXMusic.utils.formatters import get_readable_time


@app.on_message(filters.video_chat_started, group=20)
@app.on_message(filters.video_chat_ended, group=30)
async def welcome(_, message: Message):
    await Anony.stop_stream_force(message.chat.id)


@app.on_message(
    ~filters.me & ~filters.private & ~filters.bot & ~filters.via_bot,
    group=7,
)
async def chat_watcher_func(_, message: Message):
    if not message.from_user:
        return
    userid = message.from_user.id
    user_name = ("@" + message.from_user.username) if message.from_user.username else message.from_user.first_name
    if message.entities:
        possible = ["/afk", f"/afk@{app.username}"]
        message_text = message.text or message.caption
        try:
            for entity in message.entities:
                if entity.type == MessageEntityType.BOT_COMMAND:
                    if (message_text[0 : 0 + entity.length]).lower() in possible:
                        return
        except:
            pass

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time(int(time.time() - timeafk))
            if afktype == "text":
                msg += f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n"
            elif afktype == "text_reason":
                msg += f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}\n\n"
            elif afktype == "animation":
                if not reasonafk:
                    send = await message.reply_animation(
                        data,
                        caption=f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n",
                    )
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}\n\n",
                    )
            elif afktype == "photo":
                if not reasonafk:
                    send = await message.reply_photo(
                        data,
                        caption=f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n",
                    )
                else:
                    send = await message.reply_photo(
                        data,
                        caption=f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}\n\n",
                    )
            elif afktype == "sticker":
                if os.path.exists(f"downloads/{userid}.jpg"):
                    med = f"downloads/{userid}.jpg"
                else:
                    med = await app.download_media(data, file_name=f"{userid}.jpg")
                if not reasonafk:
                    send = await message.reply_photo(
                        photo=med,
                        caption=f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n",
                    )
                else:
                    send = await message.reply_photo(
                        photo=med,
                        caption=f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}\n\n",
                    )
        except:
            msg += f"{user_name} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ !"
        
    # Replied to a User which is AFK
    if message.reply_to_message:
        try:
            replied_first_name = ("@" + message.reply_to_message.from_user.username) if message.reply_to_message.from_user.username else message.reply_to_message.from_user.first_name
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time(
                        int(time.time() - timeafk)
                    )
                    if afktype == "text":
                        msg += f"{replied_first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}"
                    elif afktype == "text_reason":
                        msg += f"{replied_first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}"
                    elif afktype == "animation":
                        if not reasonafk:
                            send = await message.reply_animation(
                                data,
                                caption=f"{replied_first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                            )
                        else:
                            send = await message.reply_animation(
                                data,
                                caption=f"{replied_first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                            )
                    elif afktype == "photo":
                        if not reasonafk:
                            send = await message.reply_photo(
                                data,
                                caption=f"{replied_first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                            )
                        else:
                            send = await message.reply_photo(
                                data,
                                caption=f"{replied_first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                            )
                    elif afktype == "sticker":
                        if os.path.exists(f"downloads/{replied_user_id}.jpg"):
                            med = f"downloads/{replied_user_id}.jpg"
                        else:
                            med = await app.download_media(data, file_name=f"{replied_user_id}.jpg")
                        if not reasonafk:
                            send = await message.reply_photo(
                                photo=med,
                                caption=f"{replied_first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                            )
                        else:
                            send = await message.reply_photo(
                                photo=med,
                                caption=f"{replied_first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                            )
                except:
                    msg += f"{replied_first_name} ɪs ᴀғᴋ."
        except:
            pass

    if message.entities:
        entity = message.entities
        j = 0
        for x in range(len(entity)):
            if (entity[j].type) == MessageEntityType.MENTION:
                print(1)
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    print(2)
                    get_user = found[j]
                    user = await client.get_users(get_user)
                    print(3)
                    if user.id == replied_user_id:
                        print(4)
                        j += 1
                        continue
                except:
                    print(5)
                    j += 1
                    continue
                usern = ("@" + user.username) if user.username else user.first_name
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    print(6)
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            int(time.time() - timeafk)
                        )
                        if afktype == "text":
                            msg += f"{usern} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}"
                        elif afktype == "text_reason":
                            msg += f"{usern} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}"
                        elif afktype == "animation":
                            if not reasonafk:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"{usern} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"{usern} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                                )
                        elif afktype == "photo":
                            if not reasonafk:
                                send = await message.reply_photo(
                                    data,
                                    caption=f"{usern} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                                )
                            else:
                                send = await message.reply_photo(
                                    data,
                                    caption=f"{usern} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                                )
                        elif afktype == "sticker":
                            if os.path.exists(f"downloads/{user.id}.jpg"):
                                med = f"downloads/{user.id}.jpg"
                            else:
                                med = await app.download_media(data, file_name=f"{user.id}.jpg")
                            if not reasonafk:
                                send = await message.reply_photo(
                                    photo=med,
                                    caption=f"{usern} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=med,
                                    caption=f"{usern} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                                )
                    except:
                        msg += (
                            f"{usern} ɪs ᴀғᴋ."
                        )
            elif (entity[j].type) == MessageEntityType.TEXT_MENTION:
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = ("@" + entity[j].user.username) if entity[j].user.username else entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            int(time.time() - timeafk)
                        )
                        if afktype == "text":
                            msg += f"{first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}"
                        elif afktype == "text_reason":
                            msg += f"{first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}"
                        elif afktype == "animation":
                            if not reasonafk:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"{first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"{first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                                )
                        elif afktype == "photo":
                            if not reasonafk:
                                send = await message.reply_photo(
                                    data,
                                    caption=f"{first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                                )
                            else:
                                send = await message.reply_photo(
                                    data,
                                    caption=f"{first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                                )
                        elif afktype == "sticker":
                            if os.path.exists(f"downloads/{user_id}.jpg"):
                                med = f"downloads/{user_id}.jpg"
                            else:
                                med = await app.download_media(data, file_name=f"{user_id}.jpg")
                            if not reasonafk:
                                send = await message.reply_photo(
                                    photo=med,
                                    caption=f"{first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}",
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=med,
                                    caption=f"{first_name} ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                                )
                    except:
                        msg += f"{first_name} ɪs ᴀғᴋ."
            j += 1
    if msg != "":
        try:
            send =  await message.reply_text(
                msg, disable_web_page_preview=True
            )
            if "ʙᴀᴄᴋ ᴏɴʟɪɴᴇ" in msg:
                try:
                    os.remove(f"downloads/{message.from_user.id}.jpg")
                except:
                    pass
        except:
            return
