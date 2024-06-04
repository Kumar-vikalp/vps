import requests, re
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize your Pyrogram client
api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6519800359:AAG-j7GxjjftXlgBpMs2AcxmlfCkf3abPI0"

app = Client("PrimeVideo", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]


@app.on_message(filters.command('start'))
async def start_msg(bot, message):
    user_name = message.from_user.first_name
    welcome_msg = (
        f"Hey {user_name}! 🌟\n\n"
        "Welcome to Prime Video Poster bot🎬\n\n"
        "Curious about a movie or show? Just send its name, and I'll fetch the Poster"
        "🚀 Supported Platforms: Telegram\n"
        "──────────────────"
    )
    start_image_url = "https://graph.org/file/5e92a1bfbffdd78ebb556.png"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Posters Universe™", url="https://t.me/postersuniverse")],
            [InlineKeyboardButton("Developer💡", url="https://t.me/Bae_wafa")],
        ]
    )
    await bot.send_photo(chat_id=message.chat.id,photo=start_image_url,caption=welcome_msg,reply_markup=keyboard)

                         
@app.on_message(filters.command("pv"))
async def url(bot, message):
    
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return

    if len(message.command) < 2:
        await message.reply_text("Invalid command. Please provide an PrimeVideo link.")
        return

    url = message.command[1]
    print(f"Received command with URL: {url}")

    def find_movie_id(url):
        pattern = r'/detail/([\w-]+)/?(?:/ref=.*|)$'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None

    movie_id = find_movie_id(url)

    if movie_id:
        try:
            api_url = f"https://www.primevideo.com/region/eu/api/getDetailPage/ref=aiv_DVAPI_getDetailPage?isElcano=1&titleID={movie_id}&language=en_US&sections=Btf"
            r = requests.get(api_url, headers={"Accept": "application/json"}).json()

            portrait = r['widgets']['productDetails']['detail']['images']['packshot']
            landscape = r['widgets']['productDetails']['detail']['images']['covershot']
            title = r['widgets']['productDetails']['detail']['title']
            releaseDate = r['widgets']['productDetails']['detail']['releaseDate'][-4:]

            await bot.send_message(message.chat.id, f"**PrimeVideo Poster: {landscape}\n\nPortrait: [Link]({portrait})\n\n{title} ({releaseDate})\n\ncc: @PostersUniverse**")
        except Exception as e:
            print("Error parsing data:", e)

    if movie_id:
        try:
            hi_api_url = f"https://www.primevideo.com/region/eu/api/getDetailPage/ref=aiv_DVAPI_getDetailPage?isElcano=1&titleID={movie_id}&language=hi_IN&sections=Btf"
            r = requests.get(hi_api_url, headers={"Accept": "application/json"}).json()
            h_portrait = r['widgets']['productDetails']['detail']['images']['packshot']
            h_landscape = r['widgets']['productDetails']['detail']['images']['covershot']
            h_title = r['widgets']['productDetails']['detail']['title']
            h_releaseDate = r['widgets']['productDetails']['detail']['releaseDate'][-4:]

            await bot.send_message(message.chat.id, f"**PrimeVideo Poster: {h_landscape}\n\nPortrait: [Link]({h_portrait})\n\n{title} ({h_releaseDate}) (Hindi)\n\ncc: @PostersUniverse**")
        except Exception as e:
            print("Error parsing data:", e)
@app.on_message(filters.command("extra"))
async def url(bot, message):
    
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return

    if len(message.command) < 2:
        await message.reply_text("Invalid command. Please provide an PrimeVideo link.")
        return

    url = message.command[1]
    print(f"Received command with URL: {url}")

    def find_movie_id(url):
        pattern = r'/detail/([\w-]+)/?(?:/ref=.*|)$'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None

    movie_id = find_movie_id(url)

    if movie_id:
        try:
            api_url = f"https://www.primevideo.com/region/eu/api/getDetailPage/ref=aiv_DVAPI_getDetailPage?isElcano=1&titleID={movie_id}&language=en_US&sections=Btf"
            r = requests.get(api_url, headers={"Accept": "application/json"}).json()

            portrait = r['widgets']['productDetails']['detail']['images']['packshot']
            landscape = r['widgets']['productDetails']['detail']['images']['covershot']
            title = r['widgets']['productDetails']['detail']['title']
            releaseDate = r['widgets']['productDetails']['detail']['releaseDate'][-4:]

        except Exception as e:
            print("Error parsing data:", e)

    if movie_id:
        try:
            ta_api_url = f"https://www.primevideo.com/region/eu/api/getDetailPage/ref=aiv_DVAPI_getDetailPage?isElcano=1&titleID={movie_id}&language=ta_IN&sections=Btf"
            r = requests.get(ta_api_url, headers={"Accept": "application/json"}).json()
            ta_portrait = r['widgets']['productDetails']['detail']['images']['packshot']
            ta_landscape = r['widgets']['productDetails']['detail']['images']['covershot']
            ta_title = r['widgets']['productDetails']['detail']['title']
            ta_releaseDate = r['widgets']['productDetails']['detail']['releaseDate'][-4:]

            await bot.send_message(message.chat.id, f"**PrimeVideo poster: {ta_landscape}\n\nPortrait: [Link]({ta_portrait})\n\n{title} - ({ta_releaseDate}) (Tamil)\n\ncc: @postersuniverse**")
        except Exception as e:
            print("Error parsing data:", e)

    if movie_id:
        try:
            te_api_url = f"https://www.primevideo.com/region/eu/api/getDetailPage/ref=aiv_DVAPI_getDetailPage?isElcano=1&titleID={movie_id}&language=te_IN&sections=Btf"
            r = requests.get(te_api_url, headers={"Accept": "application/json"}).json()
            te_portrait = r['widgets']['productDetails']['detail']['images']['packshot']
            te_landscape = r['widgets']['productDetails']['detail']['images']['covershot']
            te_title = r['widgets']['productDetails']['detail']['title']
            te_releaseDate = r['widgets']['productDetails']['detail']['releaseDate'][-4:]

            await bot.send_message(message.chat.id, f"**PrimeVideo poster: {te_landscape}\n\nPortrait: [Link]({te_portrait})\n\n{title} - ({te_releaseDate}) (Telugu)\n\ncc: @postersuniverse**")
        except Exception as e:
            print("Error parsing data:", e)


print("Bot started")
app.run()

