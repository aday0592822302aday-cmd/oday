import os
import asyncio
import urllib.request
import json
from telethon import TelegramClient, events

# بيانات البوت الخاصة بك
API_ID = 4146377  
API_HASH = "6d0f8a8af223a6522d598bb5207be24e"
BOT_TOKEN = "5295879870:AAG7oGEGMrTZsHh-XX9illo__XrxP410nGQ"

bot = TelegramClient('telegram_cloud_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

DOWNLOAD_DIR = "bot_downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_via_api(video_url):
    # استخدام API خارجي مستقر جداً لتوفير الروابط المباشرة وتخطي الحظر
    api_endpoint = f"https://cobalt.tools"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # إعداد الطلب سحابياً لطلب الفيديو بأعلى جودة مدمجة
    data = json.dumps({"url": video_url, "videoQuality": "720"}).encode("utf-8")
    req = urllib.request.Request(api_endpoint, data=data, headers=headers, method="POST")
    
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        
    if res_data.get("status") == "stream" or res_data.get("status") == "picker":
        direct_download_url = res_data.get("url")
        
        # تحميل الملف بشكل مؤقت سريع جداً داخل السيرفر السحابي
        file_path = os.path.join(DOWNLOAD_DIR, "video.mp4")
        urllib.request.urlretrieve(direct_download_url, file_path)
        return file_path, "Video"
    else:
        raise Exception("لم نتمكن من جلب رابط الفيديو من الخادم الخارجي.")

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("🚀 مستعد للعمل بأعلى استقرار! أرسل لي رابط فيديو من يوتيوب أو فيسبوك، وسأرسله لك مباشرة دون حظر.")

@bot.on(events.NewMessage)
async def handle_message(event):
    url = event.text
    if any(domain in url for domain in ["youtube.com", "youtu.be", "facebook.com", "fb.watch", "fb.gg"]):
        status_msg = await event.respond("⚡ جاري جلب الفيديو عبر السيرفر الخارجي بأقصى سرعة...")
        try:
            loop = asyncio.get_event_loop()
            file_path, title = await loop.run_in_executor(None, download_via_api, url)
            
            await status_msg.edit("🚀 جاري رفع الفيديو الآن إلى تيليجرام...")
            
            await bot.send_file(
                event.chat_id, 
                file_path, 
                caption="🎬 **تم التحميل بنجاح عبر السحاب**",
                supports_streaming=True
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
                
            await status_msg.delete()
            
        except Exception as e:
            await status_msg.edit(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")

print("البوت السحابي المستقر يعمل الآن...")
bot.run_until_disconnected()
            await status_msg.edit("🚀 جاري رفع الفيديو الآن إلى تيليجرام...")
            
            await bot.send_file(
                event.chat_id, 
                file_path, 
                caption=f"🎬 **{title}**",
                supports_streaming=True
            )
            
            if os.path.exists(file_path):
                os.remove(file_path)
                
            await status_msg.delete()
            
        except Exception as e:
            await status_msg.edit(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")

print("البوت المطور يعمل الآن...")
bot.run_until_disconnected()
