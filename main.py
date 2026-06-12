import os
import asyncio
from telethon import TelegramClient, events
from pytube import YouTube

# بيانات البوت الخاصة بك
API_ID = 4146377  
API_HASH = "6d0f8a8af223a6522d598bb5207be24e"
BOT_TOKEN = "5295879870:AAG7oGEGMrTZsHh-XX9illo__XrxP410nGQ"

bot = TelegramClient('telegram_cloud_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "bot_downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_youtube_video(video_url):
    # استخدام مكتبة pytube لتخطي حظر السيرفرات بذكاء
    yt = YouTube(video_url)
    # اختيار أعلى جودة مدمجة بالصوت والصورة تلقائياً (غالباً 720p) لتجنب فصل الصوت
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    file_path = stream.download(output_path=DOWNLOAD_DIR)
    return file_path, yt.title

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("🚀 مستعد للعمل! أرسل لي رابط فيديو من يوتيوب، وسأقوم بتحميله وإرساله لك كفيديو مباشر سريع جداً عبر السحاب.")

@bot.on(events.NewMessage)
async def handle_message(event):
    url = event.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = await event.respond("⏳ جاري سحب الفيديو ومعالجته سحابياً لتخطي الحظر...")
        try:
            # تشغيل التحميل في الخلفية عبر السيرفر
            loop = asyncio.get_event_loop()
            file_path, title = await loop.run_in_executor(None, download_youtube_video, url)
            
            await status_msg.edit("🚀 جاري رفع الفيديو الآن إلى تيليجرام...")
            
            # إرسال الملف كفيديو مباشر يدعم المشاهدة الفورية
            await bot.send_file(
                event.chat_id, 
                file_path, 
                caption=f"🎬 **{title}**",
                supports_streaming=True
            )
            
            # حذف الملف فوراً لتوفير المساحة والخصوصية
            if os.path.exists(file_path):
                os.remove(file_path)
                
            await status_msg.delete()
            
        except Exception as e:
            await status_msg.edit(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")

print("البوت المحدث يعمل الآن بنجاح...")
bot.run_until_disconnected()
