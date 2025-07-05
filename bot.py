from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

pending_users = {}

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        add_user(kk.id)

        share_link = f"https://t.me/share/url?url=%E0%B4%AE%E0%B5%80%E0%B4%A1%E0%B4%BF%E0%B4%AF%20%E0%B4%AA%E0%B5%8B%E0%B4%B8%E0%B5%8D%E0%B4%B1%E0%B5%8D%E0%B4%B1%E0%B5%8D%20%E0%B4%9A%E0%B5%86%E0%B4%AF%E0%B5%8D%E0%B4%AF%E0%B5%81%E0%B4%A8%E0%B5%8D%E0%B4%A8%E0%B4%B5%E0%B5%BC%20%E0%B4%AE%E0%B4%BE%E0%B4%A4%E0%B5%8D%E0%B4%B0%E0%B4%82%20%E0%B4%95%E0%B4%AF%E0%B4%B1%E0%B4%BF%E0%B4%95%E0%B5%8D%E0%B4%95%E0%B5%8B%20%0A%F0%9F%93%A5%20%20t.me/%2BsVf-EO-XSuA0NzY1%20%F0%9F%93%A5%0A%F0%9F%93%A5%C2%A0%20t.me/%2BsVf-EO-XSuA0NzY1%20%F0%9F%93%A5"
        pending_users[kk.id] = op.id

        await app.send_message(
            kk.id,
            f"🚨 To join **{op.title}**,**ഇതു മീഡിയ പോസ്റ്റിങ് ഉള്ള ഗ്രൂപ്പ് ആണ് ഇപ്പോൾ മീഡിയ ഗ്രൂപ്പുകൾ തുടർച്ചയായി ബാൻ ആവുന്നതുകൊണ്ടു  ഈ ഗ്രൂപ്പിന്റെ ലിങ്ക് 3 പേർക്ക് അയച്ചു കൊടുത്താൽ മാത്രമേ Approove ആവുകയുള്ളൂ**.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Share Now", url=share_link)],
                [InlineKeyboardButton("Try Again", callback_data="try_join_again")]
            ])
        )
    except errors.PeerIdInvalid:
        print("User has not started the bot yet.")
    except Exception as err:
        print(str(err))

@app.on_callback_query(filters.regex("try_join_again"))
async def try_again_check(_, cb: CallbackQuery):
    user_id = cb.from_user.id

    await cb.answer("❗️ 𝐍𝐨 𝐔𝐬𝐞𝐫 𝐉𝐨𝐢𝐧𝐞𝐝 𝐁𝐲 𝐘𝐨𝐮𝐫 𝐋𝐢𝐧𝐤𝐬 𝐒𝐡𝐚𝐫𝐞 𝐀𝐠𝐚𝐢𝐧 𝐀𝐧𝐝 𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧 ❗️", show_alert=True)
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def op(_, m :Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except:
            await m.reply("**Make Sure I Am Admin In Your Channel**")
            return 
        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]]
        ) 
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join My Update Channel To Use Me.If You Joined The Channel Then Click On Check Again Button To Confirm.**", reply_markup=key)
        return 
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("⚜️ 𝐎𝐖𝐍𝐄𝐑  ⚜️", url="https://t.me/CLUBXA"),
            InlineKeyboardButton("𝐃𝐄𝐕 🧑‍💻", url="https://t.me/DUNEBOTS")
        ]]
    )
    add_user(m.from_user.id)
    await m.reply_photo("https://graph.org/file/fa9a4b4f0b1078f2c4dbe-bdd9ea0c0eda33117c.jpg", caption="**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @CLUBXA __**".format(m.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)
    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer("🙅‍♂️ You are not joined my channel first join channel then check again. 🙅‍♂️", show_alert=True)
        return 
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("⚜️ 𝐎𝐖𝐍𝐄𝐑  ⚜️", url="https://t.me/CLUBXA"),
            InlineKeyboardButton("𝐃𝐄𝐕 🧑‍💻", url="https://t.me/DUNEBOTS")
        ]]
    )
    add_user(m.from_user.id)
    await cb.edit_text(text="**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @CLUBXA __**".format(cb.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)
    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
