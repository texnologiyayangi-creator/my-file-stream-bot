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
    # Botni xavfsiz ishga tushirish
    await bot.start()

@app.on_event("shutdown")
async def shutdown_event():
    await bot.stop()

@bot.on_message(filters.private & (filters.video | filters.document))
async def generate_link(client, message):
    file_id = message.id
    link = f"https://{DOMAIN}/watch/{file_id}"
    await message.reply_text(f"🎬 **Video tayyor!**\n\nSmart TV manzili:\n`{link}`")

@app.get("/watch/{message_id}")
async def stream_video(message_id: int):
    async def file_generator():
        # Videoni Telegramdan oqim shaklida olish
        async for chunk in bot.stream_media(message_id):
            yield chunk
    return StreamingResponse(file_generator(), media_type="video/mp4")

@app.get("/")
async def health_check():
    return {"status": "Bot Online"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Uvicorn serverini asyncio loopi bilan ishga tushirish
    config = uvicorn.Config(app, host="0.0.0.0", port=port, loop="asyncio")
    server = uvicorn.Server(config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())
