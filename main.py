import os
import asyncio
from pyrogram import Client, filters
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

# Render uchun o'zgaruvchilar
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DOMAIN = os.environ.get("DOMAIN")

app = FastAPI()

# Botni asinxron yaratish
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup():
    await bot.start()

@app.on_event("shutdown")
async def shutdown():
    await bot.stop()

@bot.on_message(filters.private & (filters.video | filters.document))
async def handle_message(client, message):
    file_id = message.id
    # Smart TV uchun havola
    link = f"https://{DOMAIN}/watch/{file_id}"
    await message.reply_text(f"🎬 **Video tayyor!**\n\nSmart TV manzili:\n`{link}`")

@app.get("/watch/{message_id}")
async def stream_video(message_id: int):
    async def file_generator():
        # Videoni qismlarga bo'lib uzatish
        async for chunk in bot.stream_media(message_id):
            yield chunk
    return StreamingResponse(file_generator(), media_type="video/mp4")

@app.get("/")
async def index():
    return {"status": "Bot ishlamoqda!"}

async def main():
    port = int(os.environ.get("PORT", 8080))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
