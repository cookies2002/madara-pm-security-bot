import os
import sys
import json
from dotenv import load_dotenv
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
client.start()

approved_file = 'approved.json'
if not os.path.exists(approved_file):
    with open(approved_file, 'w') as f:
        json.dump([], f)

def load_approved():
    with open(approved_file, 'r') as f:
        return json.load(f)

def save_approved(data):
    with open(approved_file, 'w') as f:
        json.dump(data, f)

msg_count = {}

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def pm_handler(event):
    sender = await event.get_sender()
    if sender.bot or sender.id == (await client.get_me()).id:
        return

    approved = load_approved()
    if sender.id in approved:
        return

    msg_count[sender.id] = msg_count.get(sender.id, 0) + 1

    try:
        await event.delete()
    except:
        pass

    if msg_count[sender.id] == 1:
        await client.send_message(sender.id,
            "⚠️ 𝗣𝗠 𝗦𝗘𝗖𝗨𝗥𝗜𝗧𝗬 - 𝗪𝗔𝗥𝗡 ①\n\n"
            "🩸 𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐭𝐨 𝐭𝐞𝐱𝐭 𝐡𝐞𝐫.\n"
            "⚔️ 𝐌𝐀𝐃𝐀𝐑𝐀 𝐝𝐨𝐞𝐬𝐧'𝐭 𝐩𝐥𝐚𝐲 𝐰𝐢𝐭𝐡 𝐬𝐭𝐫𝐚𝐧𝐠𝐞𝐫𝐬.\n"
            "🔥 𝐓𝐡𝐢𝐬 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐟𝐢𝐫𝐬𝐭 𝐚𝐧𝐝 𝐨𝐧𝐥𝐲 𝐰𝐚𝐫𝐧𝐢𝐧𝐠."
        )
    elif msg_count[sender.id] == 2:
        await client.send_message(sender.id,
            "⚠️ 𝗣𝗠 𝗦𝗘𝗖𝗨𝗥𝗜𝗧𝗬 - 𝗪𝗔𝗥𝗡 ②\n\n"
            "⛔ 𝐒𝐭𝐨𝐩 𝐬𝐞𝐧𝐝𝐢𝐧𝐠 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬. 𝐘𝐨𝐮'𝐫𝐞 𝐛𝐞𝐢𝐧𝐠 𝐰𝐚𝐭𝐜𝐡𝐞𝐝.\n"
            "💀 𝐌𝐀𝐃𝐀𝐑𝐀 𝐝𝐞𝐬𝐩𝐢𝐬𝐞𝐬 𝐖𝐄𝐀𝐊 𝐚𝐭𝐭𝐞𝐦𝐩𝐭𝐬.\n"
            "⚡ 𝟏 𝐦𝐨𝐫𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 = 𝐁𝐋𝐎𝐂𝐊"
        )
    elif msg_count[sender.id] >= 3:
        try:
            await event.delete()
        except:
            pass

        await client.send_message(sender.id,
            "❌ 𝗔𝗨𝗧𝗢-𝗕𝗟𝗢𝗖𝗞𝗘𝗗 ❌\n\n"
            "🕸️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐛𝐞𝐞𝐧 𝐞𝐱𝐭𝐞𝐫𝐦𝐢𝐧𝐚𝐭𝐞𝐝 𝐛𝐲 𝐌𝐀𝐃𝐀𝐑𝐀.\n"
            "🔒 𝐅𝐔𝐓𝐔𝐑𝐄 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃.\n"
            "🔇 𝐓𝐡𝐞 𝐀𝐤𝐚𝐭𝐬𝐮𝐤𝐢 𝐝𝐨𝐧'𝐭 𝐟𝐨𝐫𝐠𝐢𝐯𝐞...\n\n"
            "🩸 𝘛𝘩𝘦 𝘳𝘦𝘢𝘭 𝘎𝘩𝘰𝘴𝘵 𝘜𝘤𝘩𝘪𝘩𝘢 — 𝘥𝘦𝘷: @Madara_Uchiha_lI"
        )
        await client(functions.contacts.BlockRequest(sender.id))
        msg_count.pop(sender.id, None)

@client.on(events.NewMessage(outgoing=True, pattern=r"/approve(?: (.+))?"))
async def approve(event):
    user = await event.get_reply_message()
    arg = event.pattern_match.group(1)

    if user:
        user_id = user.sender_id
    elif arg:
        try:
            if arg.startswith("@"):
                user_entity = await client.get_entity(arg)
                user_id = user_entity.id
            else:
                user_id = int(arg)
        except:
            await event.reply("❌ Invalid user.")
            return
    else:
        await event.reply("🔹 Usage: `/approve @username` or reply to a message.")
        return

    approved = load_approved()
    if user_id not in approved:
        approved.append(user_id)
        save_approved(approved)
        await event.reply(f"✅ Approved: `{user_id}`")
    else:
        await event.reply("✅ Already approved.")

@client.on(events.NewMessage(outgoing=True, pattern=r"/block(?: (.+))?"))
async def block(event):
    user = await event.get_reply_message()
    arg = event.pattern_match.group(1)

    if user:
        user_id = user.sender_id
    elif arg:
        try:
            if arg.startswith("@"):
                user_entity = await client.get_entity(arg)
                user_id = user_entity.id
            else:
                user_id = int(arg)
        except:
            await event.reply("❌ Invalid user.")
            return
    else:
        await event.reply("🔹 Usage: `/block @username` or reply to a message.")
        return

    approved = load_approved()
    if user_id in approved:
        approved.remove(user_id)
        save_approved(approved)
    await client(functions.contacts.BlockRequest(user_id))
    await event.reply(f"❌ Blocked: `{user_id}`")

@client.on(events.NewMessage(outgoing=True, pattern=r"/listapproved"))
async def list_approved(event):
    approved = load_approved()
    if not approved:
        await event.reply("😎 No approved users yet.")
        return
    msg = "✅ Approved Users:\n" + "\n".join([f"`{uid}`" for uid in approved])
    await event.reply(msg)

@client.on(events.NewMessage(outgoing=True, pattern=r"/restart"))
async def restart(event):
    await event.reply("♻️ Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

# 💥 MADARA-style terminal message
print("🩸 MADARA PM SECURITY BOT ACTIVATED ⚔️")
print("🔥 Guarding Her Majesty’s DMs From Spies & Simps!")
print("🕹️ Bot is running... waiting for fools to message.\n")

client.run_until_disconnected()
