import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6704421213:AAGCmjhTQUwtD_wkygbx1Ma1Iy0_W4gX0Mc'
allowed_channels = [-1002096427476, -1002052643468, -1002132991630]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def fetch_zee5_content(url):
    movie_id = url.split("/")[-1]
    api = f"https://artemis.zee5.com/artemis/apq/web_app/IN/FSCQ/{movie_id}"
    params = {
    "operationName": "FSCQ",
    "variables": f'{{"id":"{movie_id}","filter":{{"country":"IN","translation":"en","version":"1","languages":"en,kn,pa,hr"}},"collectionFilter":{{"page":1,"limit":2,"itemLimit":20,"country":"IN","translation":"en","languages":"en,kn,pa,hr"}}}}',
    "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"96ff2d31a3b4b08a1fb61068c426702101b9f96340e86f036093eaca661c57d7"}}'
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "content-type": "application/json",
        "origin": "https://www.zee5.com",
        "priority": "u=1, i",
        "referer": "https://www.zee5.com/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDI0LTA1LTI3VDA3OjUyOjUzLjc5OFoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTcxNjc5NjM3M30.tqCgiSZItRoPOKjZ2h2xGR_vzcqgRXo6Egxigl08ujM",
        "x-z5-guest-token": "8090e0d1-ee59-4747-93b6-8f3b678f6c0f"
    }

    response = requests.get(api, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        similar_content = data.get('data', {}).get('similarContent', {})
        
        title = similar_content.get('title', 'N/A')
        images = similar_content.get('image', {})
        release_date = similar_content.get('releaseDate', 'N/A')[:4]
        
        list_image = images.get('list', 'N/A')
        cover_image = images.get('cover', 'N/A')
        list_clean_image = images.get('listClean', 'N/A')
        app_cover_image = images.get('appCover', 'N/A')
        square_image = images.get('square', 'N/A')
        portrait_image = images.get('portrait', 'N/A')
        
        return (
        f"<b>Zee5 Poster: https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/list/{list_image}.jpg\n\n</b>"
        f"<b>Portrait: https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/portrait/{portrait_image}.jpg\n\n</b>"            
        f"<b>Cover: <a href='https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/cover/{cover_image}.jpg'>Link</a>\n\n</b>"
        f"<b>TV cover: <a href='https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/list_Clean/{list_clean_image}.jpg'>Link</a>\n\n</b>"
        f"<b>App Cover: <a href='https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/app_cover/{app_cover_image}.jpg'>Link</a>\n\n</b>"
        f"<b>Square: <a href='https://akamaividz2.zee5.com/image/upload/resources/{movie_id}/square/{square_image}.jpg'>Link</a>\n\n</b>"
        f"<b>{title} - ({release_date})</b>\n\n"
        "<b>cc: @postersuniverse</b>"
                )
    else:
        return f"Error: Received status code {response.status_code}"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    phot_url = "https://graph.org/file/ead01ae3b66e4f4e1e278.jpg"
    await bot.send_photo(message.chat.id, photo=phot_url, caption=
        "🎉 Welcome to the <b>Zee5 Poster bot!</b> 🎬\n\n"
        "Curious about Posters on Zee5? \nJust send the Zee5 URL with the /zee5 command.\n\n"
        "<b>Aur jo mil rha hai lelo, faltu RR MAT KRO! 💫</b>\n"
    , parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands=['zee5'])
async def send_zee5_info(message: types.Message):
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n <b><a href='https://t.me/PostersUniverse'>Posters Universe™🇮🇳</a></b>\nContact <b><a href='https://t.me/aaron_contact_bot'>ADMINS</a></b> to get the link.", parse_mode=types.ParseMode.HTML)
        return
    
    try:
        url = message.text.split(" ")[1]
    except IndexError:
        await message.reply("Please provide a ZEE5 URL after the /zee5 command.")
        return
    
    info = fetch_zee5_content(url)
    await message.reply(info, parse_mode=types.ParseMode.HTML)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
