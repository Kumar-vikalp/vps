import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

def extract_movie_id(url):
    return url.split("/")[-1]

region = "CA"

api_id = "25666579"
api_hash = "d0119c6adf24fc7984e7052dd94cea7a"
bot_token = "6722503072:AAF4yt8g7PPlrLMW0cwXzi5KPqsLPnxsXqY"

bot = Bot(token=bot_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

allowed_channels = [-1002096427476, -1002052643468, -1002132991630]

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Welcome to Disney+ Poster Bot! \nSend me a Disney+ Series URL.\n /dsnp Url")

@dp.message_handler(commands=['dsnp'])
async def url_command(message: types.Message):
    if len(message.text.split()) < 2:
        await message.answer("Please provide a URL.")
        return

    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]]
        )
        await bot.send_photo(
            message.chat.id,
            photo=photo_url,
            caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.",
            reply_markup=button
        )
        return

    url = message.text.split()[1]
    print(f"Received command with URL: {url}")

    movie_id = extract_movie_id(url)
    if "movies" in url:
        encodedXXXId = "encodedFamilyId"
        DmcXXXBundle = "DmcVideoBundle"
        programORseries = "program"
    else:
        encodedXXXId = "encodedSeriesId"
        DmcXXXBundle = "DmcSeriesBundle"
        programORseries = "series"

    try:
        res = requests.get(
            f"https://disney.content.edge.bamgrid.com/svc/content/{DmcXXXBundle}/version/5.1/region/{region}/audience/false/maturity/1850/language/en/{encodedXXXId}/{url.split('/')[-1]}"
        ).json()

        if "data" in res and DmcXXXBundle in res["data"]:
            res_data = res["data"][DmcXXXBundle]["video" if "movies" in url else "series"]

            thumbnail = res_data["image"]["tile"]["1.78"][programORseries]["default"]["url"] + "/scale?auto"
            portrait = res_data["image"]["tile"]["0.71"][programORseries]["default"]["url"]
            year = res_data["releases"][0]["releaseDate"].split("-")[0]
            title = res_data["text"]["title"]["full"][programORseries]["default"]["content"]
            logo = res_data["image"]["title_treatment"]["1.78"]["series"]["default"]["url"] + "/scale?width=1920&format=jpeg"

            message_text = f"<b>Disney+ Poster\n{thumbnail}\n\nPortrait: {portrait}\n\nLogo: {logo}\n\n{title} ({year})\n\ncc: @PostersUniverse</b>"
            await message.answer(message_text, parse_mode="HTMl")
        else:
            await message.reply("Failed to fetch data from the API.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await message.reply("Failed to fetch data from the API.")

if __name__ == "__main__":
    print("Bot Started")
    executor.start_polling(dp, skip_updates=True)
