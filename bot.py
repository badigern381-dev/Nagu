
```python
from pyrogram import Client, filters
from pyrogram.types import InputFile

# ==============================
# ಇಲ್ಲಿ ನಿನ್ನ ಮಾಹಿತಿಗಳನ್ನು ಹಾಕು 👇 
BOT_TOKEN = "6262823979:AAEZ8EbdgKWgh4BkjrAre9DxAFFhmKaNczI"
API_ID = 20754511  # my.telegram.org ನಲ್ಲಿ ಸಿಗುತ್ತದೆ
API_HASH = "024dfc58eb74589852411576d0e111d7"
# ==============================

# ಬಾಟ್ ಕ್ರಿಯೇಟ್ ಮಾಡುವುದು
app = Client("movies_request_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# ಬಾಟ್‌ಗಾಗಿ ಥಂಬರ್‌ನೆಲ್ ಇಮೇಜ್ ಮತ್ತು ಹೆಸರು
THUMBNAIL_PATH = "path_to_your_thumbnail.jpg"  # ನಿಮ್ಮ ಥಂಬರ್‌ನೆಲ್ ಇಮೇಜ್ ಗಾಗಿ ಪಥದ ಐಡಿಯಲ್ಲಿ ಬದಲಾಯಿಸಿ
NEW_BOT_NAME = "Your New Bot Name"  # ಹೊಸ ಹೆಸರು

# "/start" ಕಮಾಂಡ್‌ನ್ನು ನಿರ್ವಹಿಸಲು ಹ್ಯಾಂಡ್ಲರ್
@app.on_message(filters.command("start"))
def start(client, message):
    welcome_message = "ನಮಸ್ಕಾರ! ನಾನು Movies Request Bot. ನೀವು ಮೈಲಿ ಕೃತಿಗಳನ್ನು ಕೇಳಬಹುದು."
    client.send_message(chat_id=message.chat.id, text=welcome_message)

# ಫೈಲ್ ಅನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಲು ಫಂಕ್ಷನ್
@app.on_message(filters.command("upload"))
def upload_file(client, message):
    # ಫೈಲ್ ಮಾರ್ಗವನ್ನು ನಿರ್ಧರಿಸಿ
    file_path = "path_to_your_file.mp4"  # ಇಂಗ್ಲಿಷ್ನಲ್ಲಿ ಹೊಸ ಫೈಲ್‌ನ್ನು ಮಾರ್ಗವನ್ನು ಬದಲಾಯಿಸಿ
    
    # ಫೈಲ್ ಅನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡುವುದು
    client.send_document(chat_id=message.chat.id, document=file_path)

# ಬಾಟ್ ಹೆಸರನ್ನು ಮತ್ತು ಥಂಬರ್‌ನೆಲ್ ಅನ್ನು ಬದಲಾಯಿಸಲು
@app.on_message(filters.command("set_details"))
def set_details(client, message):
    # ಥಂಬರ್‌ನೆಲ್ ಓದಲು
    if THUMBNAIL_PATH:
        client.set_user_profile_photo(photo=InputFile(THUMBNAIL_PATH))
    
    # ಹೊಸ ಬಾಟ್ ಹೆಸರನ್ನು ಹೊಂದಿಸಲು
    client.set_my_name(NEW_BOT_NAME)
    
    client.send_message(chat_id=message.chat.id, text="ಥಂಬರ್‌ನೆಲ್ ಮತ್ತು ಹೆಸರು ಯಶಸ್ವಿಯಾಗಿ ಬದಲಾಯಿಸಲಾಯಿತು.")

# ಬಾಟ್ ಅನ್ನು ಕೆಲಸ ಮಾಡಿಸಲು
app.run()
```