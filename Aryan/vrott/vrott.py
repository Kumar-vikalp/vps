import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

# Existing functions for fetching details
def fetch_details(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def get_series_details(series_id, lang_id):
    api_url = f"https://api.vrott.tv/api/series/single/{series_id}?lang_id={lang_id}"
    return fetch_details(api_url)

def get_movie_details(movie_id, lang_id):
    api_url = f"https://api.vrott.tv/api/movie/single/{movie_id}?lang_id={lang_id}"
    return fetch_details(api_url)

# Initialize the bot
bot_token = "6259046207:AAG5ISFlGJf3dut4gfn3hhuvBwIxWNpguZ8"  # Replace this with your bot token
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

allowed_channels = [-1002052643468, -1002132991630, -1002096427476]

# Language IDs and their names
languages = {
    1: "English",
    2: "Hindi",
    7: "Tamil",
    8: "Telugu"
}

def print_details(title, release_date, card_image, banner_image, lang_name):
    output = f"<b>Vrott Poster: {banner_image}</b>\n\n<b>Portrait: {card_image}\n\n{title} - ({release_date}) {{{lang_name}}}</b>\n\n<i><b>cc: @postersuniverse</b></i>"
    return output

# Simple /start command handler
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Send a greeting message to the user
    await message.answer("Hello! I'm a Vrott.tv bot. You can use the /vrott command to fetch details of movies or series from Vrott.tv.")

@dp.message_handler(commands=['vrott'])
async def fetch_details_from_url(message: types.Message):
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup().add(InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot"))
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in Posters Universe Public Group\nContact Admins to get the link.", reply_markup=button)
        return

    url = message.text.strip()
    if "show/movie" in url or "show/series" in url:
        # Process the URL and fetch details
        if "show/movie" in url:
            movie_id = url.split("show/movie/")[-1]
            for lang_id, lang_name in languages.items():
                movie_details = get_movie_details(movie_id, lang_id)
                if movie_details:
                    title = movie_details['data']['title']
                    release_date = movie_details['data'].get('original_release_date', 'N/A')
                    card_image = movie_details['data']['images'].get('card_image', 'N/A')
                    banner_image = movie_details['data']['images'].get('banner_image', 'N/A')
                    output = print_details(title, release_date, card_image, banner_image, lang_name)
                    await message.answer(output, parse_mode=ParseMode.HTML)
        else:
            series_id = url.split("show/series/")[-1]
            for lang_id, lang_name in languages.items():
                series_details = get_series_details(series_id, lang_id)
                if series_details:
                    title = series_details['data']['title']
                    release_date = series_details['data'].get('original_release_date', 'N/A')
                    card_image = series_details['data']['images'].get('card_image', 'N/A')
                    banner_image = series_details['data']['images'].get('banner_image', 'N/A')
                    output = print_details(title, release_date, card_image, banner_image, lang_name)
                    await message.answer(output, parse_mode=ParseMode.HTML)
    else:
        await message.answer("Sorry, I can only process URLs of movies or series from Vrott.tv.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
