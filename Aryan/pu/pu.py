import requests
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6810924517:AAHSEq5251zxsE3gGxt1e_CWtSZsKXAq-cg"

tmdb_api_key = "27debbe382ef4f1493998a2e2598de95"

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]
force_join_channel = -1001934162558  # Replace with your channel ID

def get_movie_id(tmdb_link):
    return tmdb_link.split("/")[-1]

def get_movie_data(movie_id):
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": tmdb_api_key, "append_to_response": "videos,images"}
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

def get_series_data(series_id):
    base_url = f"https://api.themoviedb.org/3/tv/{series_id}"
    params = {"api_key": tmdb_api_key, "append_to_response": "videos,images"}
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

async def print_movie_data(message, tmdb_link):
    movie_id = get_movie_id(tmdb_link)
    data = get_movie_data(movie_id)
    if data:
        title = data["original_title"]
        release_date = data["release_date"]
        year = release_date.split('-')[0] if release_date else "N/A"
        portrait_path = data["poster_path"]
        backdrop_images = data["images"]["backdrops"]

        posters = [f"[Poster {i+1}](https://image.tmdb.org/t/p/original{backdrop['file_path']})" for i, backdrop in enumerate(backdrop_images) if backdrop.get("iso_639_1") == "en"]
        hindi_posters = [f"[Hindi Poster {i+1}](https://image.tmdb.org/t/p/original{backdrop['file_path']})" for i, backdrop in enumerate(backdrop_images) if backdrop.get("iso_639_1") == "hi"]

        posters_str = "**Posters:**\n" + "\n".join(posters) + "\n" if posters else ""
        hindi_posters_str = "**Hindi Posters:**\n" + "\n".join(hindi_posters) + "\n" if hindi_posters else ""
        portrait = f"\n**Portrait:**\n[{title}](https://image.tmdb.org/t/p/original{portrait_path})\n"

        output_hindi = hindi_posters_str + portrait
        output_hindi += f"\n\n**{title} ({year})**\n\ncc: @postersuniverse"
        await message.reply_text(output_hindi)

        output_english = posters_str + portrait
        output_english += f"\n\n**{title} ({year})**\n\ncc: @postersuniverse"
        await message.reply_text(output_english)
    else:
        print("No data found for this link")

async def print_series_data(message, tmdb_link):
    series_id = get_movie_id(tmdb_link)
    data = get_series_data(series_id)
    if data:
        title = data.get("name", "N/A")
        release_date = data.get("first_air_date", "N/A")
        year = release_date.split('-')[0] if release_date != "N/A" else "N/A"
        portrait_path = data.get("poster_path", "")
        backdrop_images = data["images"]["backdrops"]

        posters = [f"[Poster {i+1}](https://image.tmdb.org/t/p/original{backdrop['file_path']})" for i, backdrop in enumerate(backdrop_images) if backdrop.get("iso_639_1") == "en"]
        hindi_posters = [f"[Hindi Poster {i+1}](https://image.tmdb.org/t/p/original{backdrop['file_path']})" for i, backdrop in enumerate(backdrop_images) if backdrop.get("iso_639_1") == "hi"]

        posters_str = "**Posters:**\n" + "\n".join(posters) + "\n" if posters else ""
        hindi_posters_str = "**Hindi Posters:**\n" + "\n".join(hindi_posters) + "\n" if hindi_posters else ""
        portrait = f"\n**Portrait:**\n[{title}](https://image.tmdb.org/t/p/original{portrait_path})\n"

        output_hindi = hindi_posters_str + portrait
        output_hindi += f"\n\n**{title} ({year})**\n\ncc: @postersuniverse"
        await message.reply_text(output_hindi)

        output_english = posters_str + portrait
        output_english += f"\n\n**{title} ({year})**\n\ncc: @postersuniverse"
        await message.reply_text(output_english)
    else:
        print("No data found for this link")



@bot.on_message(filters.command('movie'))
async def movie_url(bot, message):
    if len(message.command) < 2:
        await message.reply_text("Invalid command. Please provide a TMDB movie link.")
        return

    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return

    url = message.command[1]
    await print_movie_data(message, url)

@bot.on_message(filters.command('tv'))
async def series_url(bot, message):
    if len(message.command) < 2:
        await message.reply_text("Invalid command. Please provide a TMDB series link.")
        return

    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return

    url = message.command[1]
    await print_series_data(message, url)


@bot.on_message(filters.command('start'))
def start_msg(bot, message):
    welcome_msg = (
        "Welcome to Posters Universe™! 🌌✨\n\n"
        "Explore movie and series posters from around the world.\n\n"
        "Use /movie(for movies) and /tv(for series)\n"
        "Use commands then Tmdb link!\n"
        "🚀\n"
        "──────────────────"
    )
    start_image_url = "https://telegra.ph/file/936cff960ebff35797f8e.png"  # Replace with the URL of your Netflix image

    # Define the keyboard
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Posters Universe™", url="https://t.me/postersuniverse")]]
    )

    bot.send_photo(
        chat_id=message.chat.id,
        photo=start_image_url,
        caption=welcome_msg,
        reply_markup=keyboard,
    )

print("Bot started")
bot.run()
