import time

from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.utils.database import add_afk, is_afk, remove_afk
from AnonXMusic.utils.formatters import get_readable_time


@app.on_message(filters.command(["afk"]) & ~filters.bot & ~filters.me)
async def active_afk(_, message: Message):
    if message.sender_chat:
        return
    user_id = message.from_user.id
    uname = ("@" + message.from_user.username) if message.from_user.username else message.from_user.first_name
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time(int(time.time() - timeafk))
            if afktype == "text":
                send = await message.reply_text(
                    f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    disable_web_page_preview=True,
                )
            elif afktype == "text_reason":
                send = await message.reply_text(
                    f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                    disable_web_page_preview=True,
                )
            elif afktype == "animation":
                if not reasonafk:
                    send =  await message.reply_animation(
                        data,
                        caption=f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    )
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                    )
            elif afktype == "photo":
                if not reasonafk:
                    send = await message.reply_photo(
                        photo=data,
                        caption=f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    )
                else:
                    send = await message.reply_photo(
                        data,
                        caption=f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                    )
            elif afktype == "sticker":
                if not reasonafk:
                    send = await message.reply_photo(
                        photo=await app.download_media(data, file_name=f"{user_id}.jpg"),
                        caption=f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    )
                else:
                    send = await message.reply_photo(
                        photo=await app.download_media(data, file_name=f"{user_id}.jpg"),
                        caption=f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n<b>ʀᴇᴀsᴏɴ :</b> {reasonafk}",
                    )
        except Exception as ex:
            print(ex)
            send =  await message.reply_text(
                f"{uname} ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ.",
                disable_web_page_preview=True,
            )

    send = await message.reply_text(
        f"{uname} ɪs ɴᴏᴡ ᴀғᴋ !"
    )
    if len(message.command) == 1 and not message.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and not message.reply_to_message:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif (
        len(message.command) == 1
        and message.reply_to_message.animation
    ):
        _data = message.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif (
        len(message.command) > 1
        and message.reply_to_message.animation
    ):
        _data = message.reply_to_message.animation.file_id
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.photo:
        _data = message.reply_to_message.photo.file_id
        details = {
            "type": "photo",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.photo:
        _data = message.reply_to_message.photo.file_id
        _reason = message.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif (
        len(message.command) == 1 and message.reply_to_message.sticker
    ):
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            _data = message.reply_to_message.sticker.file_id
            details = {
                "type": "sticker",
                "time": time.time(),
                "data": _data,
                "reason": None,
            }
    elif (
        len(message.command) > 1 and message.reply_to_message.sticker
    ):
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            _data = message.reply_to_message.sticker.file_id
            details = {
                "type": "sticker",
                "time": time.time(),
                "data": _data,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    await add_afk(user_id, details)
