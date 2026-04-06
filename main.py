import os
import asyncio
from pyrogram import Client, filters
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

# Sozlamalar
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DOMAIN = os.environ.get("DOMAIN")

app = FastAPI()
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup_event():
    if not bot.is_connected:
        await bot.start()

@app.on_event("shutdown")
async def shutdown_event():
    if bot.is_connected:
        await bot.stop()

@bot.on_message(filters.private & (filters.video | filters.document))
async def generate_link(client, message):
    file_id = message.id
    # Linkni chiroyli qilib yasash
    link = f"https://{DOMAIN}/watch/{file_id}"
    await message.reply_text(
        f"🎬 **Video tayyor!**\n\n"
        f"Smart TV uchun havola:\n`{link}`\n\n"
        f"**Eslatma:** Brauzerda ochilmasa, linkni nusxalab VLC pleyerga qo'ying."
    )

@app.get("/watch/{message_id}")
async def stream_video(message_id: int):
    async def file_generator():
        async for chunk in bot.stream_media(message_id):
            yield chunk
    return StreamingResponse(file_generator(), media_type="video/mp4")

@app.get("/")
async def health_check():
    return {"status": "Bot ishlayapti!"}

if __name__ == "__main__":
    # Render uchun portni sozlash
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
