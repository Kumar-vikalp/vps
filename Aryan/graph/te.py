from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6906349518:AAFCxCXt1WnfMlytKTMNHGri-NsKtongfSc"

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@bot.on_message(filters.command("start"))
def start_command(client, message):
    start_message = "Welcome! This is a bot to upload images to Graph API.\n\nTo upload an imagejust send the image link."

    bot.send_photo(
        chat_id=message.chat.id,
        photo="https://graph.org/file/23aeebc1f35056795d138.jpg",
        caption=start_message,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Developer", url="https://t.me/PostersUniverse")]])
    )


@bot.on_message(filters.text)
async def process_text(_, message):
    if message.text.startswith("http") and any(ext in message.text.lower() for ext in ['jpg', 'png', 'jpeg', 'pdf', 'doc', 'docx', 'odt', 'ppt', 'pptx', 'odp', 'xls', 'xlsx', 'ods', 'txt', 'md', 'html', 'mp3', 'wav', 'ogg', 'mp4', 'avi', 'mkv']):
        try:
            image_url = message.text

            response = requests.get(image_url)
            image_content = response.content

            api_url = "https://graph.org/upload"
            files = {"file": ("image.jpg", image_content)}
            response = requests.post(api_url, files=files)

            graph_url = response.json()[0].get('src', '')

            await message.reply_text(f"**Original Image URL: **\n{image_url}\n\n**Telegraph Link:**\nhttps://graph.org{graph_url}")
        except Exception as e:
            await message.reply_text(f"Error: {e}")


async def graph_upload_from_url(url):
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            file_content = response.content

        with open("temp_file", "wb") as temp_file:
            temp_file.write(file_content)

        with open("temp_file", "rb") as f:
            files = {"file": f}
            response = requests.post("https://graph.org/upload", files=files)
            response.raise_for_status()
            response_json = response.json()
            return response_json.get("url", "")

    except Exception as e:
        raise e
    finally:
        # Remove the temporary file
        if os.path.exists("temp_file"):
            os.remove("temp_file")


if __name__ == "__main__":
    bot.run()
