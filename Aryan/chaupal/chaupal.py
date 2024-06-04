import requests
from datetime import datetime
import re
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize your Pyrogram client
api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6447068308:AAFhNPXELJDbqqJzuOcUEelLMWqI9Er1Mkw"

app = Client("chaupal", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002052643468, -1002132991630]
force_join_channel = -1001934162558  # Replace with your channel ID

def unix_year(unix_time):
    ts = int(unix_time)/1000
    releaseYear = datetime.utcfromtimestamp(ts)
    return releaseYear.strftime('%Y')


@app.on_message()
async def fetch_movie_info(client, message):
    if message.text.startswith('/chaupal'):
        url = re.search(r'(https?://[^\s]+)', message.text)
        if url:
            url = url.group(0)
            if message.chat.id not in allowed_channels:
                photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
                button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
                await app.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
                return
            token = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyCy9pm1PChZKOULywz9FBV1QD8MLZFc35c',
                                  headers={'user-agent': 'Mozilla/5.0'}, json={"returnSecureToken": True}).json()

            id = url.strip("/").split("/")[-1]
            data = requests.get(f'https://content.chaupal.tv/asset/v2/{id}',
                                headers={'user-agent': 'Mozilla/5.0', 'authorization': f"Bearer {token['idToken']}"}).json()

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

            movie_info = f"**Chaupal Poster :** {thumbnail}\n\n**Portrait :** {portrait}\n\n**{title} ({year})**\n\n**cc: @PostersUniverse**"

            await app.send_message(message.chat.id, movie_info)
        else:
            await app.send_message(message.chat.id, "Invalid URL format. Please provide a valid URL after the command.")
    else:
        await app.send_message(message.chat.id, "Invalid command. Please use the /chaupal command followed by a URL.")


if __name__ == "__main__":
    app.run()
