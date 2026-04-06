import os
from pyrogram import Client, filters
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn
import threading

# Sozlamalar (Bularni Render'da kiritasiz)
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = FastAPI()
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & (filters.video | filters.document))
async def generate_link(client, message):
    # Render'dagi sayt manzilingiz (Buni ham Render'da kiritasiz)
    domain = os.environ.get("DOMAIN") 
    file_id = message.id
    link = f"https://{domain}/watch/{file_id}"
    await message.reply_text(f"🎬 **Video tayyor!**\n\nSmart TV uchun havola:\n`{link}`\n\n_Eslatma: Videoni ochish uchun botni o'chirmaslik kerak._")

@app.get("/watch/{message_id}")
async def stream_video(message_id: int):
    async def file_generator():
        async for chunk in bot.stream_media(message_id):
            yield chunk
    return StreamingResponse(file_generator(), media_type="video/mp4")

def run_bot():
    bot.run()

if __name__ == "__main__":
    # Botni alohida oqimda ishga tushirish
    threading.Thread(target=run_bot, daemon=True).start()
    # Web serverni ishga tushirish
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
