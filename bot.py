# ⚔️ MADARA PM SECURITY BOT ⚔️
# Author: Markus Marwin (Madara Edition)
# Description: Instantly deletes and blocks unauthorized PMs with MongoDB support.
# --------------------------------------------------------------

import os
import sys
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION, APPROVED, BLOCKED

# Initialize Telegram client
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
client.start()

# ✅ MongoDB Helper Functions
def is_approved(user_id: int) -> bool:
    return APPROVED.find_one({"user_id": user_id}) is not None

def approve_user_db(user_id: int):
    if not is_approved(user_id):
        APPROVED.insert_one({"user_id": user_id})

def remove_approval(user_id: int):
    APPROVED.delete_one({"user_id": user_id})

def list_approved_users():
    return [u["user_id"] for u in APPROVED.find()]

def is_blocked(user_id: int) -> bool:
    return BLOCKED.find_one({"user_id": user_id}) is not None

def block_user_db(user_id: int):
    if not is_blocked(user_id):
        BLOCKED.insert_one({"user_id": user_id})

# 🚨 PM HANDLER: Auto-block unauthorized messages
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_guard(event):
    sender = await event.get_sender()
    me = await client.get_me()

    if sender.bot or sender.id == me.id:
        return

    if is_approved(sender.id):
        return

    # Try to delete incoming PM
    try:
        await event.delete()
    except:
        pass

    # ⚠️ Send unique Madara warning
    warn_message = (
        "🚫 **PM ACCESS VIOLATION DETECTED** 🚫\n\n"
        "👁️ You have entered *Madara’s Private Realm* without permission.\n"
        "💀 **Unauthorized PMs are classified as CRIMES** under Akatsuki Law.\n\n"
        "⚔️ _You have been recorded and marked for extermination._\n"
        "🔥 Lesson: *Only the chosen may speak.*\n\n"
        "🩸 **~ Ghost Uchiha Protocol Activated.**"
    )

    try:
        await client.send_message(sender.id, warn_message)
    except:
        pass

    # 🕸️ Auto-block and record in MongoDB
    try:
        await client(functions.contacts.BlockRequest(sender.id))
        block_user_db(sender.id)
        print(f"❌ Auto-blocked unauthorized user: {sender.id}")
    except Exception as e:
        print(f"⚠️ Error blocking {sender.id}: {e}")

# ✅ Approve command
@client.on(events.NewMessage(outgoing=True, pattern=r"/approve(?: (.+))?"))
async def approve_command(event):
    user = await event.get_reply_message()
    arg = event.pattern_match.group(1)

    if user:
        user_id = user.sender_id
    elif arg:
        try:
            user_entity = await client.get_entity(arg)
            user_id = user_entity.id
        except:
            await event.reply("❌ Invalid user or username.")
            return
    else:
        await event.reply("🔹 Usage: `/approve @username` or reply to a message.")
        return

    approve_user_db(user_id)
    await event.reply(f"✅ Approved user: `{user_id}`")

# ❌ Block command
@client.on(events.NewMessage(outgoing=True, pattern=r"/block(?: (.+))?"))
async def block_command(event):
    user = await event.get_reply_message()
    arg = event.pattern_match.group(1)

    if user:
        user_id = user.sender_id
    elif arg:
        try:
            user_entity = await client.get_entity(arg)
            user_id = user_entity.id
        except:
            await event.reply("❌ Invalid user or username.")
            return
    else:
        await event.reply("🔹 Usage: `/block @username` or reply to a message.")
        return

    remove_approval(user_id)
    block_user_db(user_id)

    try:
        await client(functions.contacts.BlockRequest(user_id))
    except:
        pass

    await event.reply(f"⛔ Blocked and logged: `{user_id}`")

# 📜 List approved users
@client.on(events.NewMessage(outgoing=True, pattern=r"/listapproved"))
async def list_approved_command(event):
    approved = list_approved_users()
    if not approved:
        await event.reply("😎 No approved users yet.")
        return

    msg = "✅ **Approved Users:**\n\n" + "\n".join([f"• `{uid}`" for uid in approved])
    await event.reply(msg)

# 🔁 Restart command
@client.on(events.NewMessage(outgoing=True, pattern=r"/restart"))
async def restart_command(event):
    await event.reply("♻️ Restarting MADARA Protocol...")
    os.execl(sys.executable, sys.executable, *sys.argv)

# 💥 Terminal Log
print("🩸 MADARA PM SECURITY BOT ONLINE ⚔️")
print("🔥 Unauthorized PMs = CRIME ⚔️")
print("👁️ Watching the fools who dare to text.\n")

client.run_until_disconnected()
