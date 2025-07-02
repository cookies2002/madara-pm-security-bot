from telethon import TelegramClient, events, functions
from config import API_ID, API_HASH, SESSION
import json, os

client = TelegramClient(SESSION, API_ID, API_HASH)
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
        return  # Approved user

    # Count messages
    msg_count[sender.id] = msg_count.get(sender.id, 0) + 1

    if msg_count[sender.id] == 1:
        await event.reply(
            "⚠️ 𝗣𝗠 𝗦𝗘𝗖𝗨𝗥𝗜𝗧𝗬 - 𝗪𝗔𝗥𝗡 ①\n"
            "𝒴𝑜𝓊 𝒶𝓇𝑒 𝓃𝑜𝓉 𝒶𝓅𝓅𝓇𝑜𝓋𝑒𝒹 𝓉𝑜 𝓂𝑒𝓈𝓈𝒶𝑔𝑒 𝓂𝓎 𝑔𝒾𝓇𝓁.\n"
            "𝑀𝒜𝒟𝒜𝑅𝒜 𝒲𝒜𝑅𝒩𝒮 𝒴𝒪𝒰 ❗"
        )
    elif msg_count[sender.id] == 2:
        await event.reply(
            "⚠️ 𝗣𝗠 𝗦𝗘𝗖𝗨𝗥𝗜𝗧𝗬 - 𝗪𝗔𝗥𝗡 ②\n"
            "𝒮𝓉𝑜𝓅 𝓈𝓅𝒶𝓂 𝑜𝓇 𝓎𝑜𝓊'𝓁𝓁 𝒷𝑒 𝒷𝓁𝑜𝒸𝓀𝑒𝒹.\n"
            "𝑀𝒜𝒟𝒜𝑅𝒜 𝒮𝑀𝒜𝒮𝐻𝐸𝒮 𝒮𝒫𝒴𝑆!"
        )
    elif msg_count[sender.id] >= 3:
        await event.reply("❌ 𝗔𝗨𝗧𝗢-𝗕𝗟𝗢𝗖𝗞𝗘𝗗 𝗕𝗬 𝗠𝗔𝗗𝗔𝗥𝗔 ❌")
        await client(functions.contacts.BlockRequest(sender.id))
        msg_count.pop(sender.id, None)

@client.on(events.NewMessage(outgoing=True, pattern=r"/approve"))
async def approve(event):
    user = await event.get_reply_message()
    if not user:
        await event.reply("Reply to a user to approve.")
        return
    approved = load_approved()
    if user.sender_id not in approved:
        approved.append(user.sender_id)
        save_approved(approved)
        await event.reply("✅ Approved successfully!")

@client.on(events.NewMessage(outgoing=True, pattern=r"/block"))
async def block(event):
    user = await event.get_reply_message()
    if not user:
        await event.reply("Reply to a user to block.")
        return
    approved = load_approved()
    if user.sender_id in approved:
        approved.remove(user.sender_id)
        save_approved(approved)
    await client(functions.contacts.BlockRequest(user.sender_id))
    await event.reply("❌ Blocked and removed from approved list.")

@client.on(events.NewMessage(outgoing=True, pattern=r"/listapproved"))
async def list_approved(event):
    approved = load_approved()
    if not approved:
        await event.reply("No approved users.")
        return
    msg = "✅ Approved Users:\n" + "\n".join([f"`{uid}`" for uid in approved])
    await event.reply(msg)

@client.on(events.NewMessage(outgoing=True, pattern=r"/restart"))
async def restart(event):
    await event.reply("♻️ Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

client.run_until_disconnected()
