from pyrogram import Client, filters
from urllib.parse import urlparse
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import requests

headers = {
    'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiYW5kcm9pZF90dkBhcHBsaWNhdGlvbiIsImlzc3VlZEF0IjoiMjAyNC0wNS0wOVQwNzo0NjoxNi42ODZaIiwicHJvZHVjdF9jb2RlIjoiemVlNUA5NzUiLCJ0dGwiOjg2NDAwMDAwLCJpYXQiOjE3MTUyNDA3NzZ9.pGs4T23R-rVBbpM9bjVFgU8XDUb9pxstYvB7P2dlUJo',
}

def extract_movie_id(movie_link):
    parsed_url = urlparse(movie_link)
    path_parts = parsed_url.path.split('/')
    movie_id = path_parts[-1]
    return movie_id

api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6704421213:AAGCmjhTQUwtD_wkygbx1Ma1Iy0_W4gX0Mc"

app = Client("Zee5", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]
force_join_channel = -1001934162558  # Replace with your channel ID

@app.on_message(filters.command('start'))
def start_msg(bot, message):
    user_name = message.from_user.first_name
    welcome_msg = (
        f"Hey {user_name}! 🌟\n\n"
        "Welcome to the Zee5 Poster bot🎬\n\n"
        "Curious about a movie or show on Zee5? \nJust send Zee5 URL with /zee5 command.\n\n"
        "Aur jo mil rha h lelo faltu RR MAT KRO\n"

    )
    start_image_url = "https://graph.org/file/2e961dd736a4831b560de.jpg"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Posters Universe™", url="https://t.me/postersuniverse")],
            [InlineKeyboardButton("Developer💡", url="https://t.me/Bae_wafa")]
        ]
    )
    bot.send_photo(
        chat_id=message.chat.id,
        photo=start_image_url,
        caption=welcome_msg,
        reply_markup=keyboard,
    )


# Command to handle ZEE5 movie links
@app.on_message(filters.command("zee5"))
async def handle_zee5_command(bot, message):
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return

    if len(message.command) < 2:
        await message.reply_text("Please provide a ZEE5 movie link after the command.")
        return

    movie_link = message.command[1]
    movie_id = extract_movie_id(movie_link)

    params = {
        'translation': 'en',
        'country': 'IN',
    }

    url = f'https://gwapi.zee5.com/content/tvshow/{movie_id}'
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    title = data.get('title', "")

    release_date = data.get('release_date')
    release_year = release_date.split("-")[0] if release_date else ""

    response_message = f"**Zee5 Poster : https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/list/{data['image']['list']}.jpg**\n\n"
    response_message += f"**Portrait : https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/portrait/{data['cover_image']}**\n\n"
    response_message += f"**Cover : [Link](https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/cover/{data['image']['cover']}.jpg)**\n\n"
    response_message += f"**TV cover : [Link](https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/tv_cover/{data['image']['tv_cover']}.jpg)**\n\n"
    response_message += f"**App cover : [Link](https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/app_cover/{data['image']['app_cover']}.jpg)**\n\n"
    response_message += f"**{title} - {release_year}**\n\n"
    response_message += "**cc: @postersuniverse**"

    await message.reply_text(response_message)

# Run the bot
app.run()
