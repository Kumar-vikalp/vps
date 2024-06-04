import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6961586704:AAHycFKuRg-ucT3Jy9DJ2LYvl5Z0POF4ul4"
imgur_client_id = "72348948e860f15"  # Replace with your Imgur client ID

bot = Client("jc", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]  # Replace with your channel ID


def get_movie_id(jiocinema_link):
    return jiocinema_link.split("/")[-1]

def get_movie_data(movie_id):
    base_url = "https://content-jiovoot.voot.com/psapi/voot/v1/voot-web/content/query/asset-details"
    params = {"responseType": "common", "devicePlatformType": "desktop", "ids": f"include:{movie_id}"}
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

async def is_user_member(user_id, channel_id):
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(e)
        return False

@bot.on_message(filters.command('start'))
def start(_, message):
    user_name = message.from_user.first_name
    start_message = (
        f"**Greetings, {user_name}!**\n\nI am JioCinema Poster Bot.\nYou can use the `/jc` command to get Poster."
    )
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Posters Universe™", url="https://t.me/postersuniverse")],
        ]
    )
    bot.send_photo(
        message.chat.id,
        photo="https://telegra.ph/file/284b2de01b1ebe4c175a7.png",
        caption=start_message,
        reply_markup=keyboard,
    )

def upload_image_to_imgur(image_url):
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        image_content = response.content

        # Upload the image to Imgur API
        api_url = "https://api.imgur.com/3/upload"
        headers = {"Authorization": f"Client-ID {imgur_client_id}"}
        files = {"image": image_content}
        response = requests.post(api_url, headers=headers, files=files)

        # Get the Imgur link
        data = response.json()
        if data['success']:
            imgur_url = data['data']['link']
            return imgur_url
        else:
            print("Error uploading to Imgur:", data['data']['error'])
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


@bot.on_message(filters.command('jc'))
async def jc_url(bot, message):
    if len(message.command) < 2:
        await bot.send_message(message.chat.id, "Invalid command. Please provide a JioCinema link.")
        return

    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in Posters Universe Public Group\nContact Admins to get the link.", reply_markup=button)
        return

    url = message.command[1]
    print(f"Received command with URL: {url}")
    movie_id = get_movie_id(url)
    data = get_movie_data(movie_id)

    if data:
        name, releaseYear = data["result"][0]["name"], data["result"][0]["releaseYear"]
        poster = f"https://v3img.voot.com/{data['result'][0]['imageUri']}?imformat=jpg"
        portrait = f"https://v3img.voot.com/{data['result'][0]['image3x4']}?imformat=jpg" if data['result'][0]['image3x4'] else None

        poster_imgur_url = upload_image_to_imgur(poster)

        output = f"**{poster_imgur_url}**\n\n"
        output += f"**Jio Cinema Poster: \n`{poster}`**\n\n"

        if portrait:
            output += f"**Portrait: `{portrait}`**\n\n"

        output += f"**{name} ({releaseYear})**\n\n"
        output += f"**cc: @PostersUniverse**\n"
        print(output)
        await bot.send_message(message.chat.id, output)
    else:
        print("No data found for this link")
        await bot.send_message(message.chat.id, "No data found for this link")

bot.run()