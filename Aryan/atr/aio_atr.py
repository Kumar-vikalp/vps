import os
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import filters
from pyimgur import Imgur

# Set your bot token here
BOT_TOKEN = '6818152863:AAE5H2KRhELfRvjXXwfEFNo95dXOyTm7nq0'

CLIENT_ID = "32bdedea342c6fe"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

allowed_channels = [-1002052643468, -1002132991630]
force_join = [-1001934162558]  # Replace with your channel ID

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
        return await upload_to_imgur(file_path)
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

async def upload_to_imgur(image_path):
    try:
        im = Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(image_path, title="Uploaded with PyImgur")
        return uploaded_image.link
    except Exception as e:
        print(f"Error uploading image to Imgur: {e}")
        return None

async def is_user_member(user_id, channel_id):
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        return member.status == "member" or member.status == "administrator" or member.status == "creator"
    except Exception as e:
        print(e)
        return False

@dp.message_handler(filters.Command('start'))
async def start_msg(message: types.Message):
    welcome_msg = (
        "Welcome to Atrangi Poster Bot! 🌌✨\n\n"
        "Extract movie/Posters from Atrangi re.\n\n"
        "Use /atr and atrangi re link!\n"
        "🚀\n"
    )
    start_image_url = "https://telegra.ph/file/936cff960ebff35797f8e.png"  # Replace with the URL of your image

    # Define the keyboard
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
    # Check if the message is from any of the allowed channels
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"  # URL of the picture
        button = InlineKeyboardMarkup().add(InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot"))
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in Posters Universe Public Group\nContact Admins to get the link.", reply_markup=button)
        return

    # Check if the user is a member of the specified channel
    if not await is_user_member(message.from_user.id, force_join[0]):
        photo_url = "https://graph.org/file/d875947af985bd86b632c.png"  # URL of the picture
        button = InlineKeyboardMarkup().add(InlineKeyboardButton("Posters Universe™🇮🇳", url="https://t.me/PostersUniverse"))
        await bot.send_photo(message.chat.id, photo=photo_url, caption="you are not the member of Posters Universe™🇮🇳 \nClick to join.", reply_markup=button)
        return

    # Extract movie ID from the link
    try:
        movie_link = message.text.split(' ', 1)[1]
    except IndexError:
        await message.reply("Invalid command format. Please provide a valid Atrangi link after the command.")
        return

    parts = movie_link.split('/')
    movie_id = parts[-1] if parts[-1] else parts[-2]

    if not movie_id:
        await message.reply("Invalid movie link. Please provide a valid Atrangi link.")
        return
    
    api_url = f"https://gway.atrangii.in/r/api/ullu2/media/getMediaByTitleYearSlugAndFamilySafe/cdiOpn?familySafe=no&titleYearSlug={movie_id}"

    response = requests.get(api_url)
    data = response.json()

    posters = data.get("mainContent", {}).get("contentMetaData", {}).get("posters", [])
    image_folder = "atrangi_images"
    os.makedirs(image_folder, exist_ok=True)

    landscape_url = ""
    portrait_url = ""
    square_url = ""

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
    year = datetime.strptime(release_date, "%Y-%m-%d %H:%M:%S").year

    landscape_graph_url = await graph_upload_from_file(landscape_url)
    portrait_graph_url = await graph_upload_from_file(portrait_url)
    square_graph_url = await graph_upload_from_file(square_url)

    graph_message = f"<b>Graph Posters</b>\n\n" \
                    f"<b>Landscape:\nhttps://graph.org{landscape_graph_url}</b>\n\n" \
                    f"<b>Portrait:\nhttps://graph.org{portrait_graph_url}</b>\n\n" \
                    f"<b>Square:\nhttps://graph.org{square_graph_url}</b>\n\n" \
                    f"<b>{title_year_slug} - {year}</b>\n\n" \
                    f"<i><b>cc: @postersuniverse</b></i>"

    await message.reply(graph_message, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
