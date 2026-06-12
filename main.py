import os
import asyncio
from telethon import TelegramClient, events
from yt_dlp import YoutubeDL

# بيانات البوت الخاصة بك
API_ID = 4146377  
API_HASH = "6d0f8a8af223a6522d598bb5207be24e"
BOT_TOKEN = "5295879870:AAG7oGEGMrTZsHh-XX9illo__XrxP410nGQ"

bot = TelegramClient('telegram_cloud_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# مجلد مؤقت لحفظ الفيديوهات أثناء رفعها
DOWNLOAD_DIR = "bot_downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_video(video_url):
    # إعدادات متطورة لتحميل أفضل جودة مدمجة mp4 لتجنب مشاكل دمج الصوت
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(info)
        return file_path, info.get('title', 'Video')

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("🚀 مرحباً بك! أرسل لي رابط فيديو من يوتيوب أو فيسبوك، وسأقوم بتحميله وإرساله لك كفيديو مباشر سريع جداً.")

@bot.on(events.NewMessage)
async def handle_message(event):
    url = event.text
    if any(domain in url for domain in ["youtube.com", "youtu.be", "facebook.com", "fb.watch", "fb.gg"]):
        status_msg = await event.respond("⏳ جاري سحب الفيديو ومعالجته عبر السيرفر الخارجي...")
        try:
            # تشغيل التحميل في الخلفية عبر السيرفر دون استهلاك إنترنت هاتفك
            loop = asyncio.get_event_loop()
            file_path, title = await loop.run_in_executor(None, download_video, url)
            
            await status_msg.edit("🚀 جاري رفع الفيديو الآن إلى تيليجرام...")
            
            # إرسال الملف الفعلي كفيديو مباشر يدعم المشاهدة الفورية
            await bot.send_file(
                event.chat_id, 
                file_path, 
                caption=f"🎬 **{title}**",
                supports_streaming=True
            )
            
            # تنظيف السيرفر وحذف الملف فوراً لتوفر المساحة والخصوصية
            if os.path.exists(file_path):
                os.remove(file_path)
                
            await status_msg.delete()
            
        except Exception as e:
            await status_msg.edit(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")

print("البوت المعدل يعمل الآن بنجاح...")
bot.run_until_disconnected()
