from TelegramBot.version import __python_version__, __version__, __pyro_version__


COMMAND_TEXT = """🗒️ Documentation for commands available to user's 

• /start: To Get start message and help guide. 

• /alive: To check if bot is alive or not.

• /paste: paste text in katb.in website.

• /screenshot or /ss: Generates Screenshot from video file

• /mediainfo or /m: Generates Mediainfo of file. 

• /sample or /trim: Generates Video sample file from a video.

"""

ABOUT_CAPTION = f"""• Python version : {__python_version__}
• Bot version : {__version__}
• pyrogram  version : {__pyro_version__}

**Developer**: https://t.me/PostersUniverse"""

START_ANIMATION = "https://graph.org/file/ead01ae3b66e4f4e1e278.jpg"

START_CAPTION = """ Hello There! I am a Telegram Bot which can generate screenshots from video files, trim sample video files, and create mediainfo for Telegram files, Direct download links and Google Drive links.\n\nPress commands button to know more about bot commands and its usage."""
