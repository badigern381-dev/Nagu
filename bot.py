import os
import logging
from pyrogram import Client, filters
from pymongo import MongoClient

# ಲಾಗಿಂಗ್ ಸೆಟ್ಟಿಂಗ್ಸ್
logging.basicConfig(level=logging.INFO)

# --- Environment Variables (Render ನಿಂದ ಪಡೆಯಲು) ---
# API ID, API HASH, ಮತ್ತು BOT_TOKEN ಅನ್ನು Render ನ Environment Variables ನಲ್ಲಿ ನಮೂದಿಸಿರಬೇಕು.
API_ID = os.getenv("API_ID") 
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN") 

# --- MongoDB Connection URL (ಪಾಸ್ವರ್ಡ್ ಸೇರಿಸಲಾಗಿದೆ) ---
# ದಯವಿಟ್ಟು <ECFONSRI9YqMPIJZ> ಜಾಗದಲ್ಲಿ ನಿಮ್ಮ ನಿಜವಾದ ಪಾಸ್ವರ್ಡ್ ಹಾಕಿ.
MONGO_URL = "mongodb+srv://badigern381_db_user:<ECFONSRI9YqMPIJZ>@cluster0.fdxreju.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# --- MongoDB ಸಂಪರ್ಕ ಕೋಡ್ ---
try:
    if not MONGO_URL or "<YOUR_MONGO_PASSWORD_HERE>" in MONGO_URL:
        # ಪಾಸ್ವರ್ಡ್ ಬದಲಾಯಿಸದಿದ್ದರೆ ಎಚ್ಚರಿಕೆ ನೀಡಿ
        raise ValueError("MongoDB URL is incorrect or password is not replaced in the code.")
        
    mongo_client = MongoClient(MONGO_URL)
    db = mongo_client["MoviesYourRequestBot"] 
    users = db["users"] 
    
    print("✅ MongoDB ಗೆ ಯಶಸ್ವಿಯಾಗಿ ಸಂಪರ್ಕಗೊಂಡಿದೆ.") 

except Exception as e:
    print(f"❌ MongoDB ಸಂಪರ್ಕ ದೋಷ: {e}. ದಯವಿಟ್ಟು ಕೋಡ್‌ನಲ್ಲಿನ MONGO_URL ಪಾಸ್‌ವರ್ಡ್ ಸರಿಯಾಗಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ.")
    # ಸಂಪರ್ಕ ವಿಫಲವಾದರೆ ಬೋಟ್ ಅನ್ನು ಸ್ಥಗಿತಗೊಳಿಸಿ
    exit()

# --- Pyrogram ಬೋಟ್ ಕ್ಲೈಂಟ್ ---
# API ID ಮತ್ತು API HASH ಇಲ್ಲದಿದ್ದರೆ ಬೋಟ್ ಪ್ರಾರಂಭವಾಗುವುದಿಲ್ಲ.
if not API_ID or not API_HASH or not BOT_TOKEN:
    print("❌ API/BOT ವಿವರಗಳು ಕಾಣೆಯಾಗಿವೆ. Render ನ Environment Variables ಪರಿಶೀಲಿಸಿ.")
    exit()

try:
    # API_ID ಅನ್ನು ಪೂರ್ಣಾಂಕವಾಗಿ (integer) ಪರಿವರ್ತಿಸುವುದು ಮುಖ್ಯ
    bot = Client(
        "MoviesYourRequestBot",  # ಸೆಷನ್ ಹೆಸರು
        api_id=int(API_ID),      
        api_hash=API_HASH, 
        bot_token=BOT_TOKEN 
    )
except ValueError:
    print("❌ API_ID ಸರಿಯಾದ ಸಂಖ್ಯೆಯಾಗಿಲ್ಲ. Render ನಲ್ಲಿ API_ID ಮೌಲ್ಯವನ್ನು ಪರಿಶೀಲಿಸಿ.")
    exit()


# --- ಆಜ್ಞೆಗಳು (Commands) ---

# /start ಆಜ್ಞೆ
@bot.on_message(filters.command("start") & filters.private)
def start_command(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಬಳಕೆದಾರರನ್ನು ಸೇರಿಸಿ
    user_data = {
        "user_id": user_id,
        "username": message.from_user.username or "N/A",
        "first_name": user_name
    }
    
    if users.find_one({"user_id": user_id}) is None:
        users.insert_one(user_data)
        
    message.reply_text(f"ನಮಸ್ಕಾರ {user_name}! 👋\nನಿಮಗೆ ಬೇಕಾದ ಚಲನಚಿತ್ರದ ಹೆಸರನ್ನು ಇಲ್ಲಿ ಕಳುಹಿಸಿ.")

# /status ಆಜ್ಞೆ (ಬೋಟ್‌ನ ಸ್ಥಿತಿ ಮತ್ತು ಬಳಕೆದಾರರ ಸಂಖ್ಯೆ)
@bot.on_message(filters.command("status") & filters.private)
def status_command(client, message):
    try:
        count = users.count_documents({})
        message.reply_text(f"ಬೋಟ್ ಚಾಲನೆಯಲ್ಲಿದೆ. ✅\nಒಟ್ಟು ನೋಂದಾಯಿತ ಬಳಕೆದಾರರು (Total users): **{count}**", parse_mode="markdown")
    except Exception as e:
        message.reply_text(f"❌ ಸ್ಥಿತಿ ಪರಿಶೀಲನೆ ವಿಫಲವಾಗಿದೆ: {e}")

# --- ಬೋಟ್ ಅನ್ನು ರನ್ ಮಾಡಿ ---
print("✅ ಬೋಟ್ ಪ್ರಾರಂಭವಾಗುತ್ತಿದೆ...")
bot.run()
