from pyrogram import Client, filters
from pymongo import MongoClient
import os

# Heroku Config Vars ನಿಂದ ಅಗತ್ಯ ಮೌಲ್ಯಗಳನ್ನು ಪಡೆಯುವುದು
API_ID = os.getenv("API_ID") 
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
mongodb_url=mongodb+srv://badigern381_db_user:<ECFONSRI9YqMPIJZ>@cluster0.fdxreju.mongodb.net/?retryWrites=true&w=majority

# --- MongoDB ಸಂಪರ್ಕ ---
try:
    mongo_client = MongoClieesyourrequest?retryWrites=true&w=majority&appName=Cluster0")

# --- MongoDB ಸಂಪರ್ಕ ---
try:
    mongo_client = MongoClient(MONGO_URL)
    # Database ಹೆಸರು: moviesyourrequest
    db = mongo_client["moviesyourrequest"]
    users = db["users"]
    print("✅ MongoDB ಗೆ ಯಶಸ್ವಿಯಾಗಿ ಸಂಪರ್ಕಗೊಂಡಿದೆ.")
except Exception as e:
    print(f"❌ MongoDB ಸಂಪರ್ಕ ದೋಷ: {e}. ದಯವಿಟ್ಟು MONGO_URL ಪರಿಶೀಲಿಸಿ.")
    exit()

# --- Pyrogram ಬಾಟ್ ಸೆಟಪ್ ---
bot = Client(
    "MoviesYourRequestBot", # Session Name
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start ಕಮಾಂಡ್ ಹ್ಯಾಂಡ್ಲರ್
@bot.on_message(filters.command("start") & filters.private)
def start(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # ಬಳಕೆದಾರರನ್ನು database ನಲ್ಲಿ ಸೇರಿಸುವುದು/ಅಪ್ಡೇಟ್ ಮಾಡುವುದು
    users.update_one(
        {"_id": user_id}, 
        {"$set": {"name": user_name, "username": message.from_user.username}}, 
        upsert=True
    )
    
    message.reply_text(
        "🎬 **ನಮಸ್ಕಾರ!** ಇದು Movies Your Request ಬಾಟ್ 🎥\n\n"
        "ಬಾಟ್ ಈಗ ಲೈವ್ ಆಗಿದೆ. /status ಕಳುಹಿಸಿ."
    )

# /status ಕಮಾಂಡ್ ಹ್ಯಾಂಡ್ಲರ್
@bot.on_message(filters.command("status") & filters.private)
def status(client, message):
    try:
        count = users.count_documents({})
        message.reply_text(f"👥 **ಒಟ್ಟು ಬಳಕೆದಾರರು (Total users):** {count} ಜನ")
    except Exception as e:
        message.reply_text(f"❌ status ಪಡೆಯುವಾಗ ದೋಷ: {e}")

# ಬಾಟ್ ಅನ್ನು ಪ್ರಾರಂಭಿಸಿ
print("🚀 ಬಾಟ್ ರನ್ ಆಗುತ್ತಿದೆ...")
bot.run()
      
