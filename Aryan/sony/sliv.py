from pyrogram import Client, filters
import requests
import re
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6978708215:AAGy8s838nSlO3NID9rKS8vMQZC4G4vbcWs"

bot = Client("Sonyliv", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]
force_join_channel = -1001934162558  # Replace with your channel ID

def get_sonyliv_info(url):
    res = requests.get("https://www.sonyliv.com/", headers={
        "user-agent": "Mozilla/5.0 (Linux; Android 11; M2101K7BI Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36"
    }).text
    token = re.findall(r'securityToken:\{value:\{resultCode:"OK",message:"",errorDescription:"200-10000",resultObj:"(.*?)"', res)[0]

    metadata_url = f'https://apiv2.sonyliv.com/AGL/2.6/A/ENG/MWEB/IN/WB/DETAIL/{url.strip("/").split("-")[-1]}'
    metadata = requests.get(metadata_url, headers={'security_token': token}).json()["resultObj"]['containers'][0]['metadata']

    portrait = metadata['emfAttributes']['portrait_thumb']
    landscape = metadata['emfAttributes']['landscape_thumb']
    title = metadata['title']
    release_year = f"({metadata.get('emfAttributes').get('release_year')})"

    return f"**Sonyliv Poster: {landscape}\n\nPortrait: {portrait}\n\n{title} {release_year}\n\ncc: @PostersUniverse**"

@bot.on_message(filters.command('start'))
def start(_, message):
    user_name = message.from_user.first_name
    start_message = (
        f"**Greetings, {user_name}!**\n\nI am Sonyliv Poster Bot.\nYou can use the `/sony` command to get a Poster.\n\n**Currently it is working for movies only**"
    )
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💡 Developer", url="https://t.me/Bae_wafa")],
            [InlineKeyboardButton("Posters Universe™", url="https://t.me/postersuniverse")]
        ]
    )
    bot.send_photo(
        message.chat.id,
        photo="https://telegra.ph/file/936cff960ebff35797f8e.png",
        caption=start_message,
        reply_markup=keyboard
    )

    
@bot.on_message(filters.command("sony", prefixes="/") )
async def sonyliv_command(client, message):
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return

    # Check if the command contains a valid URL
    if len(message.text.split()) < 2:
        await message.reply_text("Please provide a valid SonyLiv URL after the command.")
        return

    url = message.text.split(" ", 1)[1]

    # Get information and send the response
    info = get_sonyliv_info(url)
    await message.reply_text(info)


if __name__ == "__main__":
    bot.run()
