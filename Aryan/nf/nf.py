from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
import requests, re

bot = Client('netflixbot2',
             api_id = "25666579",
             api_hash = "d0119c6adf24fc7984e7052dd94cea7a",
             bot_token='6715972434:AAEHM1851TGzFUZ2MRoqz4czhdvZ5WS4Z-Y',
             workers=50,
             sleep_threshold=6)

allowed_channels = [-1002052643468, -1002132991630, -1002096427476]

def get_id(url):
    pattern = r'(\d+)'

    # Use re.search to find the match
    match = re.search(pattern, url)
    if match:
        # Extract the ID from the match
        title_id = match.group(1)
        return title_id
    else:
        return None
    
def hin(url):
        cookies = {
            'netflix-sans-normal-3-loaded': 'true',
            'netflix-sans-bold-3-loaded': 'true',
            'nfvdid': 'BQFmAAEBEPKXr7N__FSnfvwZbl-SrPtgixnoyVQ3htQhd2qBozvcwLmfnUx93IfaSIVkHYLtIjXLmf9qNy37-EpBRTS32SROjJebsC4rWE6xDXverJrS3_VnR2nuiOBR1dfovtvloPmIsZDRO1hnuN4F-WA5il68',
            'SecureNetflixId': 'v%3D2%26mac%3DAQEAEQABABQaSPoQxbZg5rC_TMw1YqYbqfvAg0e7AcM.%26dt%3D1702792662217',
            'NetflixId': 'ct%3DBQAOAAEBELwL-I4V2F3fXraPYof4TEOB8GpdBQ1gcUA0VdUeZ-hTUmCXNcpKVCrJf1yA47S2FvAiar1l-4wLYnre_umBNnCa1SrvztGCooSEvTMrFOZKvT-BHQXeLI03uZKF07FI-T1_zUnZ2GUZd5dGYB3h_weZqrg95k3gmvcb4CV4XZVb0ElDyRTScRpmnzNZVL0eNNJVWVOx7TDqoyvCepYXjbOc7RHxGS3_wl06JojAthWkHbQsDxt0sqPzwZ3FVm_p1aq240SF7R08BwH-Dw9mVTDYfxAk5rIPQI5nwN-i2MQn6YKtKiN7t-Egxds0NE2vvyJ5voOReBYgUSOEyT4GHw0gIy0rndobfDTCGAsT6BK9hOKtRqlyu9djN0xUcZaVSbLLU-EjtWEdPLBQswpMQSo8PsNT9I3lo_oie2DN6qb-5KeS6d5JeDo2V2NOc6fOMk06M2TSkCUp3-n1NbZldd0AI9fWmIc4gVv6PHAKcsbMsV35YovO-RILAuaMwzIZpXZz3XRYcvi-ZF9svrqOrkG_iwMT7NidmaSWsMJcNPCcR5OtWMe5Jux-MJJu5yAvFKR094RXr2g5GgTwZLADClCXw0Wp-AQ4PBgxL2KOXi9n3YfRMiuDd6VVenxCjC6OdWwPYFjJLoXC32e-mu1MzkTcvN86Fb7d4iztXS4uimCM6lQ.%26bt%3Ddbl%26ch%3DAQEAEAABABQMXDZepI7ECjh9c8nCyc21ncM0xsmjJyI.%26v%3D2%26mac%3DAQEAEAABABTCUHbdRklwccpWG8lE9mXRLAH2fNRx-Uk.',
            'profilesNewSession': '0',
            'OptanonConsent': 'isGpcEnabled=0&datestamp=Sun+Dec+17+2023+14%3A38%3A23+GMT%2B0530+(India+Standard+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=1e1c3ef0-eca4-4a4e-8052-7f334107c8f2&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
        }

        headers = {
            'authority': 'www.netflix.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            # 'cookie': 'netflix-sans-normal-3-loaded=true; netflix-sans-bold-3-loaded=true; nfvdid=BQFmAAEBEPKXr7N__FSnfvwZbl-SrPtgixnoyVQ3htQhd2qBozvcwLmfnUx93IfaSIVkHYLtIjXLmf9qNy37-EpBRTS32SROjJebsC4rWE6xDXverJrS3_VnR2nuiOBR1dfovtvloPmIsZDRO1hnuN4F-WA5il68; SecureNetflixId=v%3D2%26mac%3DAQEAEQABABQaSPoQxbZg5rC_TMw1YqYbqfvAg0e7AcM.%26dt%3D1702792662217; NetflixId=ct%3DBQAOAAEBELwL-I4V2F3fXraPYof4TEOB8GpdBQ1gcUA0VdUeZ-hTUmCXNcpKVCrJf1yA47S2FvAiar1l-4wLYnre_umBNnCa1SrvztGCooSEvTMrFOZKvT-BHQXeLI03uZKF07FI-T1_zUnZ2GUZd5dGYB3h_weZqrg95k3gmvcb4CV4XZVb0ElDyRTScRpmnzNZVL0eNNJVWVOx7TDqoyvCepYXjbOc7RHxGS3_wl06JojAthWkHbQsDxt0sqPzwZ3FVm_p1aq240SF7R08BwH-Dw9mVTDYfxAk5rIPQI5nwN-i2MQn6YKtKiN7t-Egxds0NE2vvyJ5voOReBYgUSOEyT4GHw0gIy0rndobfDTCGAsT6BK9hOKtRqlyu9djN0xUcZaVSbLLU-EjtWEdPLBQswpMQSo8PsNT9I3lo_oie2DN6qb-5KeS6d5JeDo2V2NOc6fOMk06M2TSkCUp3-n1NbZldd0AI9fWmIc4gVv6PHAKcsbMsV35YovO-RILAuaMwzIZpXZz3XRYcvi-ZF9svrqOrkG_iwMT7NidmaSWsMJcNPCcR5OtWMe5Jux-MJJu5yAvFKR094RXr2g5GgTwZLADClCXw0Wp-AQ4PBgxL2KOXi9n3YfRMiuDd6VVenxCjC6OdWwPYFjJLoXC32e-mu1MzkTcvN86Fb7d4iztXS4uimCM6lQ.%26bt%3Ddbl%26ch%3DAQEAEAABABQMXDZepI7ECjh9c8nCyc21ncM0xsmjJyI.%26v%3D2%26mac%3DAQEAEAABABTCUHbdRklwccpWG8lE9mXRLAH2fNRx-Uk.; profilesNewSession=0; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+17+2023+14%3A38%3A23+GMT%2B0530+(India+Standard+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=1e1c3ef0-eca4-4a4e-8052-7f334107c8f2&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        nf_url = url
        nfid = get_id(nf_url)

        params = {
            'movieid': f'{nfid}',
            'isVolatileBillboardsEnabled': 'false',
            'hasVideoMerchInBob': 'false',
        }
        try:
            response = requests.get(
                'https://www.netflix.com/nq/website/memberapi/va7b420b8/metadata',
                params=params,
                cookies=cookies,
                headers=headers,
            )
            try:
                    year = response.json()['video']['seasons'][0]['year']
            except KeyError:
                    year = response.json()['video']['year']
            # year = response.json()['video']['seasons'][0]['year']
            title = response.json()['video']['title']
            img_url = response.json()['video']['artwork'][0]['url']
            boxart_url = response.json()['video'].get('boxart', [{}])[0].get('url', 'N/A')
            return  year, title, img_url, boxart_url
    
        except KeyError:
            response = requests.get(f"https://www.netflix.com/nq/website/memberapi/va7b420b8/pathEvaluator?&original_path=/shakti/mre/pathEvaluator?&path=[%22videos%22,{nfid},[%22boxarts%22,%20%22storyArt%22],%20[%22_426x607%22,%20%22_1920x1080%22,%20%22_1920x1080%22],%20%22jpg%22]&authURL=1703421015021.V6/YPL%20UmowgDMs3CqFJQQ4Rpac=", params=params, cookies=cookies,headers=headers,)
            landscape_img = response.json()['jsonGraph']['videos'][f"{nfid}"]['boxarts']['_426x607']['jpg']['value']['url']
            portrait_img = response.json()['jsonGraph']['videos'][f"{nfid}"]['boxarts']['_1920x1080']['jpg']['value']['url']
            return  landscape_img, portrait_img

def eng(url): 
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
        'authority': 'www.netflix.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,te;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': 'pas=%7B%22supplementals%22%3A%7B%22muted%22%3Afalse%7D%7D; netflix-sans-normal-3-loaded=true; flwssn=3d27f6f8-5d92-4db3-aac2-ae702f790ce2; netflix-sans-bold-3-loaded=true; sawContext=true; nfvdid=BQFmAAEBEAAGJFePtj0YiTe4RwsnVM5ghzGEYPwHrzr32uYhW8iXKUXuZ29NZ4w_UEaXQFWQaBTEoJT5N8-mcS_cnP40AHpIoP9V3ZiT8DCkYtR5k4LDRu2-N-l71etLQazIyq-8Des84t45lQVU0BTICRe7KzwQ; SecureNetflixId=v%3D2%26mac%3DAQEAEQABABQJ75uSzr6vsWZTg1lT1_XuAGWaYkQLpnA.%26dt%3D1702804990283; NetflixId=v%3D2%26ct%3DBQAOAAEBEAHNftgvnON4ZunnGdWPO6CB0Ev55vFrhXQX5tSBgi_Fg18ApwOfpgraU_Pa3PtMxuvO15lcWYte4MXHzl8vIKc82Qv1jUYwJzFXXvVuZsHykjhgSQ50Jkovj82jbnYwNZs1j-ATasnwxuZNFFMk93qN6G4PQO3BQFqvO0rJfp7Zwhtr3IrVtrz2JsJLhHhtfQq0woY0A_GPOEUxMM_0opAUkkDhaQEjkPPgEnK_ulT72R9N_OSFMHU7G1Z83xqMIS3cvY2RKhLs6dSUE9r3s6xwY9phA4KZDhG4CMD6nxRknQ3uFkYgLHLz1kdlAHn6DjrloTFjSlMu4QbNKM_FSIO8MD44YWRKXhziL9eV5iSWKz6Mv3l6-kylvAXATlL1Y7ur0KmE358rUWoQnthidGdYKFjHzLUBQdS_koZFMHgaicV-7mZgkGW3Gt8EzwptFi0XjWFpWeqytTeujgPX1nK840DGPUYaWtMU58kj-ZhAcKBASdNJOMfkY3Dxi82tNUz4DSikgf1CE552_RqZIubfacemdkZIp2Ewzx4txd-oosYZSOlgsu8AyRHoGEhx9v2I1o1h26duhqUlP8IVAQXtesVryKk4io_NfzwQRs41WQlVXRpXUdNueen7IU3S4_kF%26bt%3Ddbl%26ch%3DAQEAEAABABQlMS4y98RDOh668U8dLfy8vthaT6rCCVY.%26mac%3DAQEAEAABABTyqVakwUAQ8KrJ_CKultn-wNtrK_lMZUI.; profilesNewSession=0; firstLolomoAfterOnRamp=true; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+17+2023+14%3A53%3A54+GMT%2B0530+(India+Standard+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=d07f21b3-08f9-4b3e-a5e4-48705f51e4df&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    nf_url = url
    nfid = get_id(nf_url)

    params = {
        'movieid': f'{nfid}',
        'isVolatileBillboardsEnabled': 'false',
        'hasVideoMerchInBob': 'false',
    }
    try:
        response = requests.get(
            'https://www.netflix.com/nq/website/memberapi/va7b420b8/metadata',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        try:
                year = response.json()['video']['seasons'][0]['year']
        except KeyError:
                year = response.json()['video']['year']
        # year = response.json()['video']['seasons'][0]['year']
        title = response.json()['video']['title']
        img_url = response.json()['video']['artwork'][0]['url']
        boxart_url = response.json()['video'].get('boxart', [{}])[0].get('url', 'N/A')
        return  year, title, img_url, boxart_url
        
    except KeyError:
        response = requests.get(f"https://www.netflix.com/nq/website/memberapi/va7b420b8/pathEvaluator?&original_path=/shakti/mre/pathEvaluator?&path=[%22videos%22,{nfid},[%22boxarts%22,%20%22storyArt%22],%20[%22_426x607%22,%20%22_1920x1080%22,%20%22_1920x1080%22],%20%22jpg%22]&authURL=1703421015021.V6/YPL%20UmowgDMs3CqFJQQ4Rpac=", params=params, cookies=cookies,headers=headers,)
        landscape_img = response.json()['jsonGraph']['videos'][f"{nfid}"]['boxarts']['_426x607']['jpg']['value']['url']
        portrait_img = response.json()['jsonGraph']['videos'][f"{nfid}"]['boxarts']['_1920x1080']['jpg']['value']['url']
        return  landscape_img, portrait_img

@bot.on_message(filters.command('start'))
def start_msg(bot, message):
    user_name = message.from_user.first_name
    welcome_msg = (
        f"Hey {user_name}! 🌟\n\n"
        "Welcome to the Netflix Poster bot🎬\n\n"
        "Curious about a movie or show on Netflix? \nJust send Nf URL with /nf command.\n\n"
        "Aur jo mil rha h lelo faltu RR MAT KRO\n"
        "🚀 Supported Platforms: Telegram\n"
        "──────────────────"
    )
    start_image_url = "https://te.legra.ph/file/83032dd2ac03a466353f4.png"

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Posters Universe™", url="https://t.me/postersuniverse")],
            [InlineKeyboardButton("DEV💡", url="https://t.me/chromecdmmapi"), InlineKeyboardButton("DEV💡", url="https://t.me/Bae_wafa")],
        ]
    )
    bot.send_photo(
        chat_id=message.chat.id,
        photo=start_image_url,
        caption=welcome_msg,
        reply_markup=keyboard,
    )

@bot.on_message(filters.command('nf'))
async def nf_url(bot, message):
    if message.chat.id not in allowed_channels:
        photo_url = "https://graph.org/file/088ef13acf7c36aacd916.png"
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Admin Contact Bot", url="https://t.me/aaron_contact_bot")]])
        await bot.send_photo(message.chat.id, photo=photo_url, caption="This command is only available in\n **Posters Universe Public Group**\nContact **Admins** to get the link.", reply_markup=button)
        return

    url = message.command[1]
    hi_poster = hin(url)
    en_poster = eng(url)

    try:
        hi_boxart_url, hi_poster_url, hi_title, hi_year = hi_poster[3], hi_poster[2], hi_poster[1], hi_poster[0]
        en_boxart_url, en_poster_url, en_title, en_year = en_poster[3], en_poster[2], en_poster[1], en_poster[0]

        msg2 = (
            f"**Netflix Poster: {hi_poster_url}**\n\n"
            f"**Portrait: [Link]({hi_boxart_url})**\n\n"
            f"**{en_title} ({hi_year}) (Hindi)\n\ncc: @PostersUniverse**"
        )
        msg = (
            f"**Netflix Poster: {en_poster_url}**\n\n"
            f"**Portrait: [Link]({en_boxart_url})**\n\n"
            f"**{en_title} ({en_year})**\n\n**cc: @PostersUniverse**"
        )

        await message.reply_text(msg, quote=True)
        await message.reply_text(msg2, quote=True)

    except IndexError:
        hi_portrait_url, hi_landscape_url = hi_poster[0], hi_poster[1]
        en_portrait_url, en_landscape_url = en_poster[0], en_poster[1]

        msg2 = (
            f"**Netflix Poster:**\n{hi_landscape_url}**\n\n"
            f"**Portrait: [Link]({hi_portrait_url})\n\n**cc: @PostersUniverse**"
        )
        msg = (
            f"**Netflix Poster:\n{en_landscape_url}\n\n**"
            f"**Portrait: [Link]({en_portrait_url})**\n\n**cc: @PostersUniverse**"
        )

        await message.reply_text(msg, quote=True)
        await message.reply_text(msg2, quote=True)

print("Bot Started")
bot.run()
