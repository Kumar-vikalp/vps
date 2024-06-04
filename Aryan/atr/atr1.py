import os
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import filters
from pyimgur import Imgur

BOT_TOKEN = '6818152863:AAE5H2KRhELfRvjXXwfEFNo95dXOyTm7nq0'
CLIENT_ID = "32bdedea342c6fe"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]


async def download_image_with_extension(image_url, filename, extension=".jpg"):
    response = requests.get(image_url)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image_path = os.path.join("atrangi_images", filename)
        image.save(image_path)
        return image_path
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")
        return None

async def graph_upload_from_file(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post("https://graph.org/upload", files=files)
            response.raise_for_status()
            response_json = response.json()

            if response_json and response_json[0].get("src"):
                return response_json[0].get("src", "")
            else:
                raise ValueError("Invalid response format from graph.org")

    except Exception as e:
        raise e
async def is_user_member(user_id, channel_id):
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(e)
        return False

@dp.message_handler(filters.Command('start'))
async def start_msg(message: types.Message):
    welcome_msg = (
        "Welcome to Atrangii Poster Bot! 🌌✨\n\n"
        "Extract movie/Posters from Atrangii.\n\n"
        "Use /atr and atrangii link!\n"
        "🚀\n"
    )
    start_image_url = "https://telegra.ph/file/936cff960ebff35797f8e.png"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Posters Universe™", url="https://t.me/postersuniverse")]]
    )

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=start_image_url,
        caption=welcome_msg,
        reply_markup=keyboard,
    )

@dp.message_handler(filters.Command('atr'))
async def cmd_atr(message: types.Message):
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup().add(InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot"))
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in Posters Universe Public Group\nContact Admins to get the link.", reply_markup=button)
        return


    try:
        movie_link = message.text.split(' ', 1)[1]
    except IndexError:
        await message.reply("Invalid command format. Please provide a valid Atrangii link after the command.")
        return

    parts = movie_link.split('/')
    movie_id = parts[-1] if parts[-1] else parts[-2]

    if not movie_id:
        await message.reply("Invalid movie link. Please provide a valid Atrangii link.")
        return
    
    api_url = f"https://gway.atrangii.in/r/api/ullu2/media/getMediaByTitleYearSlugAndFamilySafe/cdiOpn?familySafe=no&titleYearSlug={movie_id}"

    response = requests.get(api_url)
    data = response.json()

    posters = data.get("mainContent", {}).get("contentMetaData", {}).get("posters", [])
    image_folder = "atrangi_images"
    os.makedirs(image_folder, exist_ok=True)

    landscape_url, portrait_url, square_url = "", "", ""

    for i, poster in enumerate(posters):
        file_id = poster.get("fileId", "")
        image_orientation = poster.get("imageOrientation", "")
        image_url = f"https://media-files.atrangii.in{file_id}"
        filename = f"{movie_id}_{image_orientation.lower()}.png"

        downloaded_image_path = await download_image_with_extension(image_url, filename, extension=".png")

        if image_orientation == "LANDSCAPE":
            landscape_url = downloaded_image_path
        elif image_orientation == "PORTRAIT":
            portrait_url = downloaded_image_path
        elif image_orientation == "SQUARE":
            square_url = downloaded_image_path

    content_metadata = data.get("mainContent", {}).get("contentMetaData", {})
    release_date = content_metadata.get("releaseDate", "")
    title_year_slug = content_metadata.get("titleYearSlug", "")

    # Format title_year_slug
    title_year_slug = title_year_slug.replace("-", " ").capitalize()
    if release_date:
        title_year_slug = f"{title_year_slug} - ({release_date.split('-')[0]})"

    landscape_graph_url = await graph_upload_from_file(landscape_url)
    portrait_graph_url = await graph_upload_from_file(portrait_url)
    square_graph_url = await graph_upload_from_file(square_url)

    graph_message = f"<b>Atrangii Posters</b>\n\n" \
                    f"<b>Landscape:\nhttps://graph.org{landscape_graph_url}</b>\n\n" \
                    f"<b>Portrait:\nhttps://graph.org{portrait_graph_url}</b>\n\n" \
                    f"<b>Square:\nhttps://graph.org{square_graph_url}</b>\n\n" \
                    f"<b>{title_year_slug}</b>\n\n" \
                    f"<i><b>cc: @postersuniverse</b></i>"

    await message.reply(graph_message, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
