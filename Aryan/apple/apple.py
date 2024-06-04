import requests
import re
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize your Pyrogram client
api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6987775755:AAGkwC0JI5f1EN_mPTB4vNjnvGd-HVF49Ng"

app = Client("apple", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]

def unix_year(unix_time):
    ts = int(unix_time)/1000
    releaseYear = datetime.utcfromtimestamp(ts)
    return releaseYear.strftime('%Y')

async def fetch_data_from_api(url):
    try:
        response = requests.get(url).json()
        return response
    except Exception as e:
        print("Error fetching data from API:", e)
        return None

@app.on_message(filters.command("apple"))
async def url(bot, message):
    
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return
    
    if len(message.command) < 2:
        await message.reply_text("Invalid command. Please provide an Apple link.")
        return

    url = message.command[1]
    print(f"Received command with URL: {url}")

    try:
        r = requests.get(f"https://appleapi.trendyfilms.workers.dev/?url={url}").json()
        if re.match(r"https?://tv\.apple\.com/[a-z]{2}/show/", url.split("?url=")[-1]):
            titleInfo = list(r.keys())[1]
        else:
            titleInfo = list(r.keys())[0]
        id = r[titleInfo]
        tvs_id = next(iter(id['playables']))
        title = id['content']['title']
        year = unix_year(id["content"]["releaseDate"])

        portrait = id['playables'][tvs_id]['images']['coverArt']['url'].format(w="2000", h="3000", f='jpg')
        landscape = id['content']['images']['posterArt']['url'].format(w="3840", h="2160", f='jpg')

        print(f"{landscape}\n\nPortrait :- {portrait}\n\n{title} ({year})")
        await bot.send_message(message.chat.id, f"**Apple poster: {landscape}\n\nPortrait: [Link]({portrait})\n\n{title} ({year})\n\ncc: @postersuniverse**")
    except Exception as e:
        error_message = "An error occurred with the custom API: {}".format(e)
        await message.reply_text(error_message)

# Start the client
print("Bot Started")
app.run()
