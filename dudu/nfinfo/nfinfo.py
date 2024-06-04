import requests,re
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode

# Function to extract ID from URL
def get_id(url):
    match = re.search(r'(\d+)', url)
    return match.group(1) if match else None

# Function to get data from APIs
def get_data(url):
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjY3OTYyOCwianRpIjoiMjA0ZjllOGYtZDI1Mi00ZmRkLTkxYzktNDIyOGZjMmIzYmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE3MTY2Nzk2MTEuMjA0IiwibmJmIjoxNzE2Njc5NjI4LCJleHAiOjE3MTY3NjYwMjh9.mh4z-bbuAKrqjvG8tjAETeXLIWecKxFaFwIKRTof144",
        "cookie": "authtoken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjY3OTYyOCwianRpIjoiMjA0ZjllOGYtZDI1Mi00ZmRkLTkxYzktNDIyOGZjMmIzYmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE3MTY2Nzk2MTEuMjA0IiwibmJmIjoxNzE2Njc5NjI4LCJleHAiOjE3MTY3NjYwMjh9.mh4z-bbuAKrqjvG8tjAETeXLIWecKxFaFwIKRTof144; eucookie=stupideulaw; countrylist=46",
        "priority": "u=1, i",
        "referer": "https://unogs.com/search/new%20last%2024%20hours",
        "referrer": "http://unogs.com",
        "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def get_url_from_message(message):
    return message.get_args()

# Initialize bot and dispatcher
API_TOKEN = '7119798462:AAEU4rXBdkMMmghNxfnskYhVdrBcW3pi-mA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Command handler for /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm your Netflix bot. You can use /info to get Netflix information.")

# Command handler for /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("To use this bot, simply type /info to get Netflix information.")

@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    url = get_url_from_message(message)
    if not url:
        await message.reply("Please provide a Netflix URL with the /info command.")
        return

    nfid = get_id(url)
    if not nfid:
        await message.reply("Invalid URL. Please provide a valid Netflix URL.")
        return

    api1 = f"https://unogs.com/api/title/detail?netflixid={nfid}"
    api2 = f"https://unogs.com/api/title/countries?netflixid={nfid}"

    data1, data2 = get_data(api1), get_data(api2)
    if not (isinstance(data1, list) and data1 and isinstance(data2, list) and data2):
        await message.reply("No data available.")
        return

    x1, x2 = data1[0], data2[0]
    title, lgimg = x1.get("title"), x1.get("lgimg")
    netflix_id, vtype, nfdate = x1.get("netflixid"), x1.get("vtype"), x1.get("nfdate")
    country, cc = x2.get("country"), x2.get("cc")
    audio = ', '.join([audio.split(' - ')[0] for audio in x2.get("audio", "").split(',') if "Audio Description" not in audio])

    country_emoji = get_country_emoji(cc)
    country_info = f"{country} {country_emoji}" if country_emoji else country

    caption = (
    f"🎬 <b>Title:</b> {title}\n"
    f"🆔 <b>Netflix ID:</b><code> {netflix_id}</code>\n"
    f"📺 <b>Type:</b> {vtype}\n"
    f"🌍 <b>Country:</b> {country_info}\n"
    f"🔠 <b>Country Code (cc):</b> {cc}\n"
    f"🔊 <b>Audio:</b> {audio}"
    )

    await bot.send_photo(message.chat.id, lgimg, caption=caption, parse_mode=ParseMode.HTML)

def get_country_emoji(country_code):
    base, offset = ord(country_code[0]) - ord('A') + 0x1F1E6, ord(country_code[1]) - ord('A') + 0x1F1E6
    return chr(base) + chr(offset) if 'A' <= country_code[0] <= 'Z' and 'A' <= country_code[1] <= 'Z' else ''


@dp.message_handler(commands=['search'])
async def search_movie(message: types.Message):
    query = message.get_args()
    if not query:
        await message.reply("Please provide a movie name with the /search command.")
        return

    url = 'https://unogs.com/api/search'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjY3OTYyOCwianRpIjoiMjA0ZjllOGYtZDI1Mi00ZmRkLTkxYzktNDIyOGZjMmIzYmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE3MTY2Nzk2MTEuMjA0IiwibmJmIjoxNzE2Njc5NjI4LCJleHAiOjE3MTY3NjYwMjh9.mh4z-bbuAKrqjvG8tjAETeXLIWecKxFaFwIKRTof144',
        'cookie': 'authtoken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjY3OTYyOCwianRpIjoiMjA0ZjllOGYtZDI1Mi00ZmRkLTkxYzktNDIyOGZjMmIzYmI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjE3MTY2Nzk2MTEuMjA0IiwibmJmIjoxNzE2Njc5NjI4LCJleHAiOjE3MTY3NjYwMjh9.mh4z-bbuAKrqjvG8tjAETeXLIWecKxFaFwIKRTof144; eucookie=stupideulaw; countrylist=46',
        'priority': 'u=1, i',
        'referer': f'https://unogs.com/search/{query}?countrylist=46',
        'referrer': 'http://unogs.com',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'x-requested-with': 'XMLHttpRequest'
    }

    params = {
        'limit': 1,
        'offset': 0,
        'query': query,
        'countrylist': 46
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        if results:
            first_result = results[0]
            title = first_result.get('title', 'N/A')
            nfid = first_result.get('nfid', 'N/A')
            vtype = first_result.get('vtype', 'N/A')
            year = first_result.get('year', 'N/A')
            poster = modify_poster_url(first_result.get('poster', 'N/A')) if first_result.get('poster') else 'N/A'
            country_list = process_country_list(first_result.get('clist', 'N/A'))
            
            caption = (
                        f"🎬 <b>Title:</b> {title}\n"
                        f"🆔 <b>Netflix ID:</b><code> {nfid}</code>\n"
                        f"📺 <b>Type:</b> {vtype}\n"
                        f"📅 <b>Year:</b> {year}\n"
                        f"🌍 <b>Country List:</b> {country_list}"
                        )
            
            await bot.send_photo(chat_id=message.chat.id, photo=poster, caption=caption, parse_mode=ParseMode.HTML)
        else:
            await message.reply("No results found.")
    else:
        await message.reply(f'Error: {response.status_code}')

def modify_poster_url(url):
    parts = url.split('.')
    if len(parts) > 2:
        return '.'.join(parts[:-2]) + '.jpg'
    return url

def get_country_emoji(country_code):
    return chr(ord(country_code[0]) - ord('A') + 0x1F1E6) + chr(ord(country_code[1]) - ord('A') + 0x1F1E6)

def process_country_list(country_list):
    countries = re.findall(r'"(.*?)":"(.*?)"', country_list)
    processed_list = [f"{get_country_emoji(code)} {name}" for code, name in countries]
    
    more_countries = re.search(r'\"more\":\"(\+\d+)\"', country_list)
    if more_countries:
        processed_list.append(more_countries.group(1))

    return ', '.join(processed_list)

def get_id(url):
    match = re.search(r'(\d+)', url)
    return match.group(1) if match else None


def get_netflix_data(url):
    nfid = get_id(url)
    if not nfid:
        raise ValueError("Invalid Netflix URL. Please provide a valid Netflix URL.")

    api_url = f'https://www.netflix.com/shakti/mre/pathEvaluator?hasVideoMerchInBob=true&path=["videos",{nfid},"bobSummary"]&authURL=1704968105302.gfHxptX9wE5SmOztUvgRig6JxVQ='
    cookies = {
        'pas': '%7B%22supplementals%22%3A%7B%22muted%22%3Afalse%7D%7D',
        'netflix-sans-normal-3-loaded': 'true',
        'flwssn': '3d27f6f8-5d92-4db3-aac2-ae702f790ce2',
        'netflix-sans-bold-3-loaded': 'true',
        'sawContext': 'true',
        'nfvdid': 'BQFmAAEBEAAGJFePtj0YiTe4RwsnVM5ghzGEYPwHrzr32uYhW8iXKUXuZ29NZ4w_UEaXQFWQaBTEoJT5N8-mcS_cnP40AHpIoP9V3ZiT8DCkYtR5k4LDRu2-N-l71etLQazIyq-8Des84t45lQVU0BTICRe7KzwQ',
        'SecureNetflixId': 'v%3D2%26mac%3DAQEAEQABABQJ75uSzr6vsWZTg1lT1_XuAGWaYkQLpnA.%26dt%3D1702804990283',
        'NetflixId': 'v%3D2%26ct%3DBQAOAAEBEAHNftgvnON4ZunnGdWPO6CB0Ev55vFrhXQX5tSBgi_Fg18ApwOfpgraU_Pa3PtMxuvO15lcWYte4MXHzl8vIKc82Qv1jUYwJzFXXvVuZsHykjhgSQ50Jkovj82jbnYwNZs1j-ATasnwxuZNFFMk93qN6G4PQO3BQFqvO0rJfp7Zwhtr3IrVtrz2JsJLhHhtfQq0woY0A_GPOEUxMM_0opAUkkDhaQEjkPPgEnK_ulT72R9N_OSFMHU7G1Z83xqMIS3cvY2RKhLs6dSUE9r3s6xwY9phA4KZDhG4CMD6nxRknQ3uFkYgLHLz1kdlAHn6DjrloTFjSlMu4QbNKM_FSIO8MD44YWRKXhziL9eV5iSWKz6Mv3l6-kylvAXATlL1Y7ur0KmE358rUWoQnthidGdYKFjHzLUBQdS_koZFMHgaicV-7mZgkGW3Gt8EzwptFi0XjWFpWeqytTeujgPX1nK840DGPUYaWtMU58kj-ZhAcKBASdNJOMfkY3Dxi82tNUz4DSikgf1CE552_RqZIubfacemdkZIp2Ewzx4txd-oosYZSOlgsu8AyRHoGEhx9v2I1o1h26duhqUlP8IVAQXtesVryKk4io_NfzwQRs41WQlVXRpXUdNueen7IU3S4_kF%26bt%3Ddbl%26ch%3DAQEAEAABABQlMS4y98RDOh668U8dLfy8vthaT6rCCVY.%26mac%3DAQEAEAABABTyqVakwUAQ8KrJ_CKultn-wNtrK_lMZUI.',
        'profilesNewSession': '0',
        'firstLolomoAfterOnRamp': 'true',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Sun+Dec+17+2023+14%3A53%3A54+GMT%2B0530+(India+Standard+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=d07f21b3-08f9-4b3e-a5e4-48705f51e4df&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    params = {
        'movieid': f'{nfid}',
        'isVolatileBillboardsEnabled': 'false',
        'hasVideoMerchInBob': 'false',
    }
    response = requests.get(api_url, headers=headers, params=params, cookies=cookies)
    return response.json()


@dp.message_handler(commands=['trailer'])
async def send_trailer(message: types.Message):
    try:
        url = message.text.split(' ')[1]
        netflix_data = get_netflix_data(url)
        video_data = netflix_data['value']['videos'][str(get_id(url))]['bobSummary']
        video_id = video_data['videoId']
        title = video_data['title']
        video_type = video_data['type']
        box_art_url = video_data['boxArt']['url']
        availability_date = video_data['availability']['availabilityDate']
        tags = ", ".join(video_data['evidence']['tags']['value'])
        logo_image_url = video_data['logoImage']['url']
        trailer_id = video_data['videoMerch']['id']
        
        caption = (
                f"🎬 <b>Title:</b> {title}\n"
                f"🆔 <b>Netflix ID:</b><code> {video_id}</code>\n"
                f"🎞️ <b>Trailer ID:</b><code> {trailer_id}</code>\n"
                f"📺 <b>Type:</b> {video_type}\n"
                f"📅 <b>Availability Date:</b> {availability_date}\n"
                f"🏷️ <b>Tags:</b> {tags}\n"

                )
        # Sending Box Art URL as a photo
        box_art_response = requests.get(box_art_url)
        if box_art_response.status_code == 200:
            # Sending Box Art image as a photo with caption
            await bot.send_photo(message.chat.id, box_art_response.content, caption=caption, parse_mode=ParseMode.HTML)
        else:
            await message.reply("Failed to fetch Box Art image.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
