import os
import sqlite3
import telebot
from telebot import types

BOT_TOKEN = "8844366383:AAEMOIQfan451s4UYTOd0Qmu6VEUOSnWvu0"
ADMIN_ID = 6051956660

bot = telebot.TeleBot(BOT_TOKEN)

# DATABASE SETUP
conn = sqlite3.connect('mhn_users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (tg_id INTEGER PRIMARY KEY, name TEXT, age TEXT, city TEXT, photo_id TEXT)''')
conn.commit()

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.city = None
        self.photo_id = None

# START COMMAND
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, "🏹 **မြှားနက်မောင် သူငယ်ချင်းရှာဖွေရေးမှ ကြိုဆိုပါတယ်!**\n\nသူငယ်ချင်းအသစ်တွေ ရှာဖို့ အရင်ဆုံး Profile ဆောက်ရအောင်နော်။ မင်းရဲ့ နာမည် (သို့မဟုတ်) နာမည်ပြောင်ကို ရိုက်ပို့ပေးပါဗျ။")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, "🔢 မင်းရဲ့ အသက်ကို ဂဏန်းလိုပဲ ရိုက်ပို့ပေးပါဦး။")
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, "❌ တစ်ခုခုမှားယွင်းသွားပါတယ်။ ကျေးဇူးပြုပြီး `/start` ကို ပြန်နှိပ်ပါ။")

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        user = user_dict[chat_id]
        user.age = age
        msg = bot.reply_to(message, "📍 မင်းအခု လက်ရှိ နေထိုင်တဲ့ မြို့ပြအမည်ကို ရိုက်ပို့ပေးပါ။")
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(message, "❌ ပြဿနာရှိလို့ `/start` ကို ပြန်နှိပ်ပေးပါ။")

def process_city_step(message):
    try:
        chat_id = message.chat.id
        city = message.text
        user = user_dict[chat_id]
        user.city = city
        msg = bot.reply_to(message, "📸 နောက်ဆုံးအဆင့်အနေနဲ့ မင်းရဲ့ ကြည့်ကောင်းတဲ့ ဓာတ်ပုံတစ်ပုံ ပို့ပေးပါဗျ။")
        bot.register_next_step_handler(msg, process_photo_step)
    except Exception as e:
        bot.reply_to(message, "❌ ပြဿနာရှိလို့ `/start` ကို ပြန်နှိပ်ပေးပါ။")

def process_photo_step(message):
    try:
        chat_id = message.chat.id
        if not message.photo:
            msg = bot.reply_to(message, "⚠️ ဓာတ်ပုံပဲ ပို့ပေးရမှာပါဗျ။ ဖိုင်မဟုတ်ဘဲ ပုံစံအတိုင်း ပြန်ပို့ပေးပါဦး။")
            bot.register_next_step_handler(msg, process_photo_step)
            return
            
        user = user_dict[chat_id]
        user.photo_id = message.photo[-1].file_id
        
        # DATABASE ထဲ သိမ်းဆည်းခြင်း
        c.execute("INSERT OR REPLACE INTO users (tg_id, name, age, city, photo_id) VALUES (?, ?, ?, ?, ?)",
                  (chat_id, user.name, user.age, user.city, user.photo_id))
        conn.commit()
        
        # အောင်မြင်ကြောင်း ပြန်ကြားခြင်း
        bot.send_photo(chat_id, user.photo_id, 
                       caption=f"🎉 **Profile ဆောက်လို့ ပြီးပါပြီ!**\n\n📝 နာမည်: {user.name}\n🔢 အသက်: {user.age}\n📍 မြို့: {user.city}\n\nမြှားနက်မောင်က သင့်တော်မယ့်သူတွေကို မကြာခင် ရှာဖွေပေးပါလိမ့်မယ်။")
        
        # Admin ဆီကို လူသစ်စာရင်းသွင်းကြောင်း အချက်ပေးခြင်း
        bot.send_message(ADMIN_ID, f"🔔 **User အသစ်တစ်ယောက် တိုးလာပါပြီ!**\nID: {chat_id}\nName: {user.name}\nAge: {user.age}\nCity: {user.city}")
    except Exception as e:
        bot.reply_to(message, "❌ မှားယွင်းမှုဖြစ်သွားလို့ အစက ပြန်လုပ်ပေးပါ။")

# ADMIN COMMAND: USER များအားလုံးကို စစ်ဆေးခြင်း
@bot.message_handler(commands=['viewusers'])
def view_users(message):
    if message.chat.id == ADMIN_ID:
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        if not rows:
            bot.send_message(ADMIN_ID, "📭 Database ထဲမှာ အခုထိ User စာရင်း မရှိသေးပါဘူး။")
            return
            
        bot.send_message(ADMIN_ID, f"📊 **စုစုပေါင်း User အရေအတွက်:** {len(rows)} ဦး\nစာရင်းများကို တစ်ပုံချင်းစီ ပို့ပေးနေပါတယ်...")
        for row in rows:
            info = f"🆔 TG ID: {row[0]}\n📝 နာမည်: {row[1]}\n🔢 အသက်: {row[2]}\n📍 မြို့: {row[3]}"
            bot.send_photo(ADMIN_ID, row[4], caption=info)
    else:
        bot.reply_to(message, "⚠️ မင်းက ဒီ Bot ရဲ့ အရှင်သခင် Admin မဟုတ်လို့ ဒီ Command သုံးခွင့်မရှိပါဘူး။")

if __name__ == "__main__":
    print("🚀 မြှားနက်မောင် Bot running...")
    bot.infinity_polling()
