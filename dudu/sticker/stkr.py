import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os
import io
from PIL import Image

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    photo_url = 'https://graph.org/file/3df765e9f722b27a13f17.jpg'
    caption = 'Hi! Send me the link to the image you want to turn into a sticker.\n\n• 𝐃ᴇᴠᴇʟᴏᴘᴇʀ: @Bae_wafa\ncc: @PostersUniverse🌿🥰'
    
    # Create an inline keyboard button
    button = InlineKeyboardButton(text="Posters Universe™🇮🇳", url='https://t.me/PostersUniverse')
    keyboard = InlineKeyboardMarkup([[button]])
    
    # Send the photo with caption and button
    context.bot.send_photo(
        chat_id=chat_id,
        photo=photo_url,
        caption=caption,
        reply_markup=keyboard
    )  

# Define the sticker command handler
def make_sticker(update, context):
    link = update.message.text
    image_content = download_image(link)
    if image_content:
        try:
            image = Image.open(io.BytesIO(image_content))
            sticker_bytes = io.BytesIO()
            image.save(sticker_bytes, format="PNG")
            sticker_bytes.seek(0)
            update.message.reply_sticker(sticker=sticker_bytes)
        except Exception as e:
            update.message.reply_text(f"Failed to process the image: {e}")
    else:
        update.message.reply_text("Please provide a valid image link.")

# Function to download image from URL
def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
        return None

# Define the main function to start the bot
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("7413943404:AAGRQNCqEnTqDcmlRFy6p79UzTJ9pitIJK4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, make_sticker))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
