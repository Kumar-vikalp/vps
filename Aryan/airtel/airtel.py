import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6657657607:AAGcNivw6J5Z81y4VAHyUAG5dhq4NauAKGQ"

app = Client("Airtel", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]

@app.on_message(filters.command("airtel"))
async def url(bot, message):
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return
    
    if len(message.command) < 2:
        await message.reply_text("Invalid command. Please provide an Airtel XStream Link.")
        return

    url = message.command[1]
    print(f"Received command with URL: {url}")

    try:
        # Extract movie ID from the URL
        def extract_movie_id(url):
            parts = url.split('/')
            return parts[-1]

        # Generate API URL
        def generate_api_url(movie_id):
            return f"https://content.airtel.tv/app/v4/content?id={movie_id}"

        # Extracting movie ID
        movie_id = extract_movie_id(url)
        # Generating API URL
        api_url = generate_api_url(movie_id)

        print("API URL:", api_url)

        # Send GET request to the API
        response = requests.get(api_url)

        # Check if request was successful
        if response.status_code == 200:
            # Extract the JSON data
            data = response.json()

            # Extracting the image URLs
            images = data.get('images', {})
            landscape_url = images.get('LANDSCAPE_169')
            feature_banner_url = images.get('FEATURE_BANNER')
            feature_banner_hd_url = images.get('FEATURE_BANNER_HD')
            portrait_url = images.get('PORTRAIT')

            # Extract other movie details
            title = data.get("title")
            release_year = data.get("releaseYear")
                # Sending the message with extracted data
            await bot.send_message(message.chat.id, f"**Airtel XStream Poster: {landscape_url}\n\nBanner: [link]({feature_banner_hd_url})\n\nPortrait: [link]({portrait_url})\n\n{title} ({release_year})\n\ncc: @postersuniverse**")
        else:
            await message.reply_text("Failed to fetch data from the API.")
    
    except Exception as e:
        error_message = "An error occurred with the custom API: {}".format(e)
        await message.reply_text(error_message)

print("Bot Started")
app.run()
