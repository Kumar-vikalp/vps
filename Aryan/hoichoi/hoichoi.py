import json
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6637428071:AAFcz6OUZUlX-oNNcLNezNpVAzn7SeqAlV4"
app = Client("hoichoi_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]

async def get_hoichoi_info(url):
    jsonData = requests.get(f'https://www.hoichoi.tv/cache/{"movies" if "movies" in url else "shows"}/{url.split("/")[-1]}', headers={"user-agent": "android"}).text
    jsonData = json.loads(jsonData)
    CON_XXX = list(jsonData.keys())[-2]
    metadata = jsonData[CON_XXX]["modules"][1]["contentData"][0]

    title = metadata["gist"]["title"]
    year = f'({metadata["gist"]["year"]})' if "movies" in url else f'- {metadata["seasons"][0]["title"]} ({metadata["showDetails"]["trailers"][0]["year"]})'
    thumbnail = metadata["gist"]["videoImageUrl"]
    portrait = metadata["gist"]["posterImageUrl"]

    return f"**HOichoi Poster : \n{thumbnail}\n\nPortrait: {portrait}\n\n{title} {year}\n\ncc: @PostersUniverse**"

@app.on_message(filters.command("hoichoi"))
async def hoichoi_info(client, message):
    if len(message.command) == 1:
        await message.reply_text("Please provide a valid URL along with the command.")
        return
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await app.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return
        
    url = message.command[1]
    hoichoi_info_result = await get_hoichoi_info(url)
    await message.reply_text(hoichoi_info_result)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Welcome to the Hoichoi Bot! \nUse the /hoichoi command + Hoichoi URL to get Poster..")

app.run()
