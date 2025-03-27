import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# 載入 .env 環境變數
load_dotenv()

# TOKEN = os.getenv("DISCORD_TOKEN")
# TARGET_TEXT_CHANNEL_ID = int(os.getenv("TEXT_CHANNEL_ID"))

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_TEXT_CHANNEL_ID = int(os.getenv("TEXT_CHANNEL_ID"))

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot 已上線：{bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        channel = bot.get_channel(TARGET_TEXT_CHANNEL_ID)
        if channel:
            await channel.send(f'🎧 {member.display_name} 加入了語音頻道：{after.channel.name}')

bot.run(TOKEN)





# 假裝有一個 HTTP server（Render 會掃這個）
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running.")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))  # Render 會給你一個 PORT
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"🌐 Fake HTTP server started on port {port}")
    server.serve_forever()

# 在背景執行 HTTP server
threading.Thread(target=run_http_server, daemon=True).start()