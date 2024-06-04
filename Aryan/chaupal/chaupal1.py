from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from datetime import datetime
import re

# Initialize your Pyrogram client
api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6447068308:AAFhNPXELJDbqqJzuOcUEelLMWqI9Er1Mkw"

app = Client("chaupal", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]

def unix_year(unix_time):
    ts = int(unix_time)/1000
    releaseYear = datetime.utcfromtimestamp(ts)
    return releaseYear.strftime('%Y')


@app.on_message(filters.command("chaupal", prefixes="/"))
async def chaupal_info(bot, message):
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return
    try:
        # Extract the URL from the command
        url = message.text.split(maxsplit=1)[1]
    except IndexError:
        # Handle case where URL is not provided
        await message.reply_text("Please provide a valid Chaupal URL after the command.")  # Await the reply_text method
        return

    # Fetch token
    token_response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyCy9pm1PChZKOULywz9FBV1QD8MLZFc35c',
                                   headers={'user-agent': 'Mozilla/5.0'},
                                   json={"returnSecureToken": True})
    
    if token_response.status_code != 200:
        # Handle error in fetching token
        message.reply_text("Failed to fetch authentication token. Please try again later.")
        return

    token = token_response.json()

    # Fetch data from Chaupal API
    id = url.strip("/").split("/")[-1]
    data_response = requests.get(f'https://content.chaupal.tv/asset/v2/{id}',
                                 headers={'user-agent': 'Mozilla/5.0',
                                          'authorization': f"Bearer {token.get('idToken', '')}"})
    
    if data_response.status_code != 200:
        # Handle error in fetching data from Chaupal API
        message.reply_text("Failed to fetch data from Chaupal API. Please try again later.")
        return

    data = data_response.json()

    # Extract necessary information
    for image in data["images"]:
        if image["type"] == "thumbnail":
            thumbnail = image["url"] + "_1050x591"
        elif image["type"] == "portrait":
            portrait = image["url"] + "_630x945"

    title = data["name"]
    try:
        year = unix_year(data["releaseDate"]["availableFrom"])
    except:
        year = data["year"]

    # Compose the response message
    response_message = f"**Chaupal Poster : {thumbnail}\n\nPortrait : {portrait}\n\n{title} - ({year})\n\ncc: @PostersUniverse**"

    # Send the response
    await message.reply_text(response_message)


print ("Bot started")
app.run()

