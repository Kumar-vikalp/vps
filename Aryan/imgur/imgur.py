# imgur_bot_update
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pyimgur
import requests

api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6754593547:AAGyQR6n-dq7nGgNDU4jiSNaYJ5Hl_71Jpc"

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

CLIENT_ID = "32bdedea342c6fe"  # Replace with your Imgur client ID
CLIENT_SECRET = "71b2c7158821b072436ea243bffb6abc98e89ecc"  # Replace with your Imgur client secret

im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)

@bot.on_message(filters.command("start"))
def start_command(client, message):
    start_message = "Welcome! This is a bot to upload images to Imgur.\n\nTo upload an image just send the image link."

    bot.send_photo(
        chat_id=message.chat.id,
        photo="https://graph.org/file/38cdd415b8313991e72a2.png",
        caption=start_message,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/Bae_wafa")]])
    )

@bot.on_message(filters.text)
def upload_image(client, message):
    image_url = message.text.strip()

    # Check if the message contains a valid URL
    if image_url.startswith("http"):
        try:
            # Send a HEAD request to get the file size
            response = requests.head(image_url)
            content_length = int(response.headers.get('Content-Length', 0))
            # Check if file size exceeds Imgur's limit (currently 10MB)
            if content_length > 10 * 1024 * 1024:
                message.reply_text("The file you are trying to upload to Imgur exceeds the size limit allowed by Imgur (10MB). Please resize or compress the image and try again.")
                return
            # Upload the file to Imgur using its URL
            uploaded_file = im.upload_image(url=image_url, title="Uploaded with PyImgur")
            if uploaded_file:
                message.reply_text(f"**Original Image URL:** {image_url}\n\n**Imgur Link:** {uploaded_file.link}")
            else:
                message.reply_text("Failed to upload image to Imgur.")
        except Exception as e:
            message.reply_text("An error occurred while uploading the image to Imgur.")
    else:
        message.reply_text("Please send a valid URL.")

# Define stop command handler
@bot.on_message(filters.command(["stop"]))
def stop_command(client, message):
    message.reply_text("Bot is stopping. Bye!")
    bot.stop()

# Run the bot
bot.run()
