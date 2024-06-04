import logging
import requests
import re
import json
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Telegram Bot Token
API_TOKEN = '6667656381:AAEUX2HCO-_N6M-tVQCSyHp19ocLonrAQ-s'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Allowed channel IDs
ALLOWED_CHANNEL_IDS = [-1002132991630,-1002052643468] # Replace with your actual channel IDs

# Scrape Amazon video details
def scrape_amazon_video(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        script_tags = soup.find_all('script', {'type': 'text/template'})

        for i, script_tag in enumerate(script_tags, 1):
            if script_tag.string:
                content = script_tag.string.strip()
                match = re.search(r'\{"props":', content)
                if match:
                    json_content = content[match.start():]
                    try:
                        data = json.loads(json_content)
                        movie_id = next(iter(data['props']['body'][0]['props']['atf']['state']['detail']['headerDetail']))
                        movie_data = data['props']['body'][0]['props']['atf']['state']['detail']['headerDetail'][movie_id]
                        
                        title = movie_data.get('title')
                        release_year = movie_data.get('releaseYear')
                        images_data = movie_data.get('images', {})

                        movie_details = {
                            'title': title,
                            'release_year': release_year,
                            'images': images_data
                        }

                        return movie_details
                    except (json.JSONDecodeError, KeyError) as e:
                        logging.error(f"Error parsing JSON content in <script type='text/template'> tag {i}: {e}")
                        return None
                else:
                    logging.info(f"No JSON content starting with '{{\"props\":' found in <script type='text/template'> tag {i}")
    else:
        logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "Hi!\n"
        "Welcome to the Amazon Prime Video Details Bot.\n"
        "Send me an Amazon Prime Video URL using the /amzn command, and I'll scrape the details for you.\n\n"
        "Here are the commands you can use:\n"
        "/start - Display this welcome message\n"
        "/help - Get help and see an example\n"
        "/amzn [URL] - Provide an Amazon Prime Video URL to get details\n\n"
        "Example:\n"
        "/amzn https://www.amazon.com/gp/video/detail/B0D2M2L96S/ref=atv_dp_share_cu_r\n\n"
        "Note: This bot will only respond to the /amzn command in specific allowed Groups/PM(s)/Channels."
    )
    await message.reply(welcome_text)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    try:
        photo_url = "https://telegra.ph/file/6e1fb0a704fea89c6462d.jpg"  # Replace with the URL of your help photo
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Contact Us", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption=f"Click on share button to copy the link \nOnly the link in format will work\nEven If it’s an Amazon link and it’s not working if u wont send the way i showed in picture it wont work\n\nEg - https://www.amazon.com/gp/video/detail/B0CNWGLCJH/ref=atv_dp_share_cu_r", reply_markup=button)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@dp.message_handler(commands=['amzn'])
async def fetch_amazon_video_details(message: types.Message):
    if message.chat.id not in ALLOWED_CHANNEL_IDS:
        await message.reply("Sorry, You're Not Allowed to Use This Command.")
        return

    url = message.get_args()
    if not url:
        await message.reply("Please provide an Amazon Prime Video URL after the /amzn command.")
        return
    
    details = scrape_amazon_video(url)
    if details:
        title = details.get('title', 'N/A')
        release_year = details.get('release_year', 'N/A')
        images = details.get('images', {})

        response = []
        if 'covershot' in images and images['covershot']:
            response.append(f"<b>Amazon Poster: {images['covershot']}</b>")
        if 'titleLogo' in images and images['titleLogo']:
            response.append(f"<b>\nLogo: {images['titleLogo']}</b>")
        if 'titleshot' in images and images['titleshot']:
            response.append(f"<b>\nPortrait: {images['titleshot']}</b>")

        response.append(f"<b>\n{title} ({release_year})</b>")
        response.append("<b>\ncc: @PostersUniverse</b>")

        await message.reply("\n".join(response), parse_mode=ParseMode.HTML)
    else:
        await message.reply("Failed to scrape the details. Please make sure the URL is correct.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
