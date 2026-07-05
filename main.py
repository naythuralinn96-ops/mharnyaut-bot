import telebot
from telebot import types
import math

# ⚠️ အရေးကြီး - မင်းရဲ့ Telegram Bot Token ကို ဒီနေရာမှာ အစားထိုးထည့်ပါ
TOKEN = "8844366383:AAEMOIQfan451s4UYTOd0Qmu6VEUOSnWvu0"
bot = telebot.TeleBot(TOKEN)

# Admin ID (မင်းရဲ့ Telegram ID ကို ဒီမှာ ပြောင်းထည့်ပါ)
ADMIN_ID = 5476707410  

# Database (လတ်တလော မှတ်ဉာဏ်ထဲသိမ်းမယ့်စနစ်)
users_db = {}  # {user_id: {profile_data}}
active_chats = {}  # {user_id: peer_id} 为 Anonymous Chat သုံးရန်

# Temporary registration states
reg_steps = {} # {user_id: {step_data}}

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    # Reset State
    reg_steps[user_id] = {}
    
    welcome_text = (
        "🏹 **မြှားနက်မောင် သမားတော်ကြီးမှ ကြိုဆိုပါတယ်!**\n\n"
        "ရည်းစားမရှိသေးတဲ့ ပျိုမေ၊ လူပျိုလူလွတ်တွေ ချိတ်ဆက်ပေးဖို့ Profile အရင်ဆောက်ကြရအောင်ဗျာ။"
    )
    bot.send_message(user_id, welcome_text, parse_mode="Markdown")
    
    # အဆင့် ၁ - လိင်အမျိုးအစား မေးခြင်း
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("👨 ယောင်္ကျားလေး", "👩 မိန်းကလေး", "🌈 LGBT+")
    bot.send_message(user_id, "👉 မင်းရဲ့ လိင်အမျိုးအစားကို ရွေးပေးပါ-", reply_markup=markup)
    reg_steps[user_id]['step'] = 'gender'

@bot.message_handler(func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'gender')
def process_gender(message):
    user_id = message.from_user.id
    reg_steps[user_id]['gender'] = message.text
    
    # အဆင့် ၂ - စိတ်ဝင်စားမှုပုံစံ မေးခြင်း
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("👨 ယောင်္ကျားလေး", "👩 မိန်းကလေး", "👫 နှစ်မျိုးလုံး (Both)", "🧑‍🤝‍🧑 B to B / G to G")
    bot.send_message(user_id, "👉 မင်းက ဘယ်လိုလူမျိုးကို စိတ်ဝင်စားတာလဲ (Preference)?", reply_markup=markup)
    reg_steps[user_id]['step'] = 'preference'

@bot.message_handler(func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'preference')
def process_preference(message):
    user_id = message.from_user.id
    reg_steps[user_id]['preference'] = message.text
    
    # အဆင့် ၃ - စိတ်ဝင်စားသည့် အသက်အပိုင်းအခြား
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("✨ ၁၈ မှ ၂၅ နှစ်", "✨ ၂၆ မှ ၃၅ 年", "✨ အသက်မရွေးပါ")
    bot.send_message(user_id, "👉 ဘယ်လို အသက်အရွယ်အပိုင်းအခြားကို ရှာချင်တာလဲ?", reply_markup=markup)
    reg_steps[user_id]['step'] = 'target_age'

@bot.message_handler(func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'target_age')
def process_target_age(message):
    user_id = message.from_user.id
    reg_steps[user_id]['target_age'] = message.text
    
    # အဆင့် ၄ - အလုပ်အကိုင် / စရိုက်စံနှုန်း
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("🩺 ဆရာဝန်/သူနာပြု", "🏫 ကျောင်းဆရာ/မ", "🌾 လယ်သမား/အခြေခံ", "🎮 Gamer")
    markup.add("💰 ငွေရှိရမယ်", "❤️ ချစ်ပေးဖို့ပဲလိုတယ်", "🤝 သူငယ်ချင်းအဖော်သက်သက်")
    bot.send_message(user_id, "👉 မင်းက ဘယ်လိုစရိုက်/အလုပ်အကိုင် ရှိတဲ့သူကို ကြိုက်တာလဲ?", reply_markup=markup)
    reg_steps[user_id]['step'] = 'occupation'

@bot.message_handler(func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'occupation')
def process_occupation(message):
    user_id = message.from_user.id
    reg_steps[user_id]['occupation'] = message.text
    
    bot.send_message(user_id, "✍️ မင်းရဲ့ နာမည်နဲ့ အသက်ကို ရိုက်ပေးပါ (ဥပမာ- အောင်အောင်, ၂၂)-")
    reg_steps[user_id]['step'] = 'name_age'

@bot.message_handler(func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'name_age')
def process_name_age(message):
    user_id = message.from_user.id
    reg_steps[user_id]['name_age'] = message.text
    
    # အဆင့် ၅ - Location စနစ် (GPS သို့မဟုတ် ရွေးချယ်မှု)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    gps_button = types.KeyboardButton(text="📍 တိုက်ရိုက် GPS ထောက်မည် (Live Location)", request_location=True)
    markup.add(gps_button)
    markup.add("🔒 စာရင်းထဲမှ ကိုယ်တိုင်ရွေးမည် (လုံခြုံရေးအရ)")
    
    bot.send_message(user_id, "🗺️ တည်နေရာ (Location) သတ်မှတ်ပါ-", reply_markup=markup)
    reg_steps[user_id]['step'] = 'location_choice'

# GPS တိုက်ရိုက်ထောက်လှမ်းခြင်းကို ဖမ်းရန်
@bot.message_handler(content_types=['location'])
def handle_gps_location(message):
    user_id = message.from_user.id
    if reg_steps.get(user_id, {}).get('step') == 'location_choice':
        reg_steps[user_id]['lat'] = message.location.latitude
        reg_steps[user_id]['lon'] = message.location.longitude
        reg_steps[user_id]['location_text'] = "📌 GPS Live Location"
        ask_photo(user_id)

@bot.message_handler(func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'location_choice')
def process_location_text(message):
    user_id = message.from_user.id
    if "စာရင်းထဲမှ" in message.text:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("ရန်ကုန်", "မန္တလေး", "မကွေး", "နေပြည်တော်", "ပဲခူး", "တခြားမြို့/ရွာ")
        bot.send_message(user_id, "👉 တိုင်းဒေသကြီး/ပြည်နယ် မြို့နယ်ကို ရွေးပေးပါ-", reply_markup=markup)
        reg_steps[user_id]['step'] = 'manual_location'
    else:
        bot.send_message(user_id, "❌ အပေါ်က ခလုတ်ကို သုံးပြီး ရွေးချယ်ပေးပါဗျာ။")

@bot.message_handler(func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'manual_location')
def process_manual_location(message):
    user_id = message.from_user.id
    reg_steps[user_id]['location_text'] = message.text
    reg_steps[user_id]['lat'] = None
    reg_steps[user_id]['lon'] = None
    ask_photo(user_id)

def ask_photo(user_id):
    bot.send_message(user_id, "📸 နောက်ဆုံးအဆင့်အနေနဲ့... မင်းရဲ့ ကြည့်ကောင်းတဲ့ Profile ဓာတ်ပုံတစ်ပုံ ပို့ပေးပါဦးဗျာ-")
    reg_steps[user_id]['step'] = 'photo'

@bot.message_handler(content_types=['photo'], func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'photo')
def process_photo(message):
    user_id = message.from_user.id
    photo_id = message.photo[-1].file_id
    
    # Save into Database
    data = reg_steps[user_id]
    users_db[user_id] = {
        'id': user_id,
        'gender': data['gender'],
        'preference': data['preference'],
        'target_age': data['target_age'],
        'occupation': data['occupation'],
        'name_age': data['name_age'],
        'location_text': data['location_text'],
        'lat': data['lat'],
        'lon': data['lon'],
        'photo': photo_id,
        'likes': set(),
        'matched': set()
    }
    
    del reg_steps[user_id] # Clean up temp state
    
    bot.send_message(user_id, "🎉 Profile ဆောက်လို့ အောင်မြင်သွားပါပြီဗျာ!")
    show_main_menu(user_id)

def show_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 ဖူးစာရှင်ရှာမယ် (Like/Pass)", "💬 Anonymous Chat ဝင်မယ်")
    markup.add("🔗 သူငယ်ချင်းများကို Share မယ်", "⭐️ Feedback ပေးရန်")
    bot.send_message(user_id, "🏹 **မြှားနက်မောင် ပင်မစာမျက်နှာ**\nအောက်က ခလုတ်တွေသုံးပြီး စမ်းသပ်နိုင်ပါပြီဗျာ-", reply_markup=markup)

# --- 🔍 TINDER STYLE LIKE/PASS SYSTEM ---
@bot.message_handler(func=lambda msg: msg.text == "🔍 ဖူးစာရှင်ရှာမယ် (Like/Pass)")
def find_match(message):
    user_id = message.from_user.id
    if user_id not in users_db:
        bot.send_message(user_id, "❌ အရင်ဆုံး /start ကိုနှိပ်ပြီး Profile ဆောက်ပေးပါဦးဗျာ။")
        return
        
    # သင့်တော်မယ့်သူ လိုက်ရှာခြင်း (ကိုယ်မဟုတ်တဲ့ တခြားသူ)
    match_found = None
    for peer_id, peer_data in users_db.items():
        if peer_id != user_id and peer_id not in users_db[user_id]['likes']:
            match_found = peer_data
            break
            
    if match_found:
        # Distance calculation if GPS available
        dist_str = ""
        if users_db[user_id]['lat'] and match_found['lat']:
            lat1, lon1 = users_db[user_id]['lat'], users_db[user_id]['lon']
            lat2, lon2 = match_found['lat'], match_found['lon']
            # Haversine Formula
            R = 6371
            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            dist_str = f"📍 မင်းနဲ့ အကွာအဝေး: {round(R * c, 1)} km"

        profile_card = (
            f"👤 နာမည်/အသက်: {match_found['name_age']}\n"
            f"🚻 လိင်အမျိုးအစား: {match_found['gender']}\n"
            f"💼 စရိုက်/အလုပ်: {match_found['occupation']}\n"
            f"🗺️ တည်နေရာ: {match_found['location_text']}\n"
            f"{dist_str}"
        )
        
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(
            types.InlineKeyboardButton("❤️ Like", callback_data=f"like_{match_found['id']}"),
            types.InlineKeyboardButton("❌ Pass", callback_data="pass_match")
        )
        bot.send_photo(user_id, match_found['photo'], caption=profile_card, reply_markup=inline_markup)
    else:
        bot.send_message(user_id, "😔 မင်းနဲ့ ကိုက်ညီမယ့် ဖူးစာရှင်အသစ် လောလောဆယ် မရှိသေးပါဘူးဗျာ။ နောက်မှ ပြန်စမ်းကြည့်ပါ!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('like_') or call.data == 'pass_match')
def handle_like_pass(call):
    user_id = call.from_user.id
    bot.delete_message(user_id, call.message.message_id)
    
    if call.data == 'pass_match':
        bot.send_message(user_id, "⏩ ကျော်လိုက်ပါပြီ။")
        find_match(call)
        return
        
    peer_id = int(call.data.split('_')[1])
    users_db[user_id]['likes'].add(peer_id)
    
    # Check Match (နှစ်ဦးနှစ်ဖက် Like မိလား စစ်မယ်)
    if user_id in users_db.get(peer_id, {}).get('likes', set()):
        users_db[user_id]['matched'].add(peer_id)
        users_db[peer_id]['matched'].add(user_id)
        
        # Notify Both Users
        bot.send_message(user_id, "🎉 **Match ဖြစ်သွားပါပြီ!** နှစ်ယောက်လုံး အပြန်အလှန် သဘောကျကြလို့ '💬 Anonymous Chat ဝင်မယ်' ကိုနှိပ်ပြီး စကားပြောနိုင်ပါပြီဗျာ!")
        bot.send_message(peer_id, "🎉 **Match ဖြစ်သွားပါပြီ!** နှစ်ယောက်လုံး အပြန်အလှန် သဘောကျကြလို့ '💬 Anonymous Chat ဝင်မယ်' ကိုနှိပ်ပြီး စကားပြောနိုင်ပါပြီဗျာ!")
    else:
        bot.send_message(user_id, "❤️ Like ပို့လိုက်ပါပြီ။")
        find_match(call)

# --- 💬 ANONYMOUS CHATROOM SYSTEM ---
@bot.message_handler(func=lambda msg: msg.text == "💬 Anonymous Chat ဝင်မယ်")
def join_chat(message):
    user_id = message.from_user.id
    if user_id in active_chats:
        bot.send_message(user_id, "❌ မင်း Chatroom ထဲ ရောက်နေပြီးသားပါ။ ထွက်ချင်ရင် /leave ကို ရိုက်ပါ။")
        return
        
    # Match ဖြစ်ထားတဲ့သူတွေထဲက အားနေတဲ့သူကို ရှာပြီး ချိတ်ဆက်ပေးခြင်း
    matched_list = users_db.get(user_id, {}).get('matched', set())
    peer_id = None
    for m_id in matched_list:
        if m_id not in active_chats and m_id in users_db:
            peer_id = m_id
            break
            
    if peer_id:
        active_chats[user_id] = peer_id
        active_chats[peer_id] = user_id
        bot.send_message(user_id, "💬 Chatroom ချိတ်ဆက်မိသွားပါပြီ။ တစ်ယောက်ကိုတစ်ယောက် မသိရဘဲ လုံခြုံစွာ စကားပြောနိုင်ပါပြီဗျာ!\n(ထွက်ချင်ရင် /leave လို့ ရိုက်ပါ)")
        bot.send_message(peer_id, "💬 Chatroom ချိတ်ဆက်မိသွားပါပြီ။ တစ်ယောက်ကိုတစ်ယောက် မသိရဘဲ လုံခြုံစွာ စကားပြောနိုင်ပါပြီဗျာ!\n(ထွက်ချင်ရင် /leave လို့ ရိုက်ပါ)")
    else:
        bot.send_message(user_id, "⏳ မင်းနဲ့ Match ဖြစ်ထားသူတွေထဲက လောလောဆယ် အားတဲ့သူ မရှိသေးပါဘူး။ စောင့်ဆိုင်းပေးပါဦးဗျာ။")

@bot.message_handler(commands=['leave'])
def leave_chat(message):
    user_id = message.from_user.id
    if user_id in active_chats:
        peer_id = active_chats[user_id]
        del active_chats[user_id]
        if peer_id in active_chats:
            del active_chats[peer_id]
        bot.send_message(user_id, "🚪 Chatroom မှ ထွက်လိုက်ပါပြီ။")
        bot.send_message(peer_id, "🚪 တစ်ဖက်လူ Chatroom မှ ထွက်သွားပါပြီ။")
        show_main_menu(user_id)
        show_main_menu(peer_id)
    else:
        bot.send_message(user_id, "❌ မင်း ဘယ် Chatroom ထဲမှာမှ မရှိနေပါဘူး။")

# Handle chatting relays
@bot.message_handler(func=lambda msg: msg.from_user.id in active_chats, content_types=['text', 'photo', 'sticker'])
def relay_message(message):
    user_id = message.from_user.id
    peer_id = active_chats[user_id]
    
    if message.text:
        bot.send_message(peer_id, message.text)
    elif message.photo:
        bot.send_photo(peer_id, message.photo[-1].file_id, caption=message.caption)
    elif message.sticker:
        bot.send_sticker(peer_id, message.sticker.file_id)

# --- 🔗 VIRAL SHARE SYSTEM ---
@bot.message_handler(func=lambda msg: msg.text == "🔗 သူငယ်ချင်းများကို Share မယ်")
def share_bot(message):
    user_id = message.from_user.id
    share_markup = types.InlineKeyboardMarkup()
    # Telegram inline share url
    bot_info = bot.get_me()
    share_url = f"https://t.me/share/url?url=https://t.me/{bot_info.username}&text=ဟေ့ကောင်တွေ... ရည်းစားမရှိသေးရင် ဒီ 'မြှားနက်မောင်' Dating Bot လေးမှာ ဖူးစာရှင် လာရှာကြဟေ့။ အလန်းစားပဲ!"
    share_markup.add(types.InlineKeyboardButton("🚀 သူငယ်ချင်းများထံ ဖိတ်ခေါ်စာ Share မည်", url=share_url))
    bot.send_message(user_id, "🔗 အောက်ကခလုတ်ကို သုံးပြီး ရည်းစားမရှိတဲ့ သူငယ်ချင်းတွေ သို့မဟုတ် Group တွေထဲကို ဒီ Bot လေးအကြောင်း လှမ်း Share နိုင်ပါတယ်ဗျာ-", reply_markup=share_markup)

# --- ⭐️ FEEDBACK & RATING SYSTEM ---
@bot.message_handler(func=lambda msg: msg.text == "⭐️ Feedback ပေးရန်")
def feedback_start(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("⭐️ 5 Stars", "⭐️ 4 Stars", "⭐️ 3 Stars", "⭐️ 2 Stars", "⭐️ 1 Star")
    bot.send_message(user_id, "🏹 မြှားနက်မောင် Bot ကို ဘယ်လောက်အဆင့် သတ်မှတ်ချင်လဲဗျာ?", reply_markup=markup)
    reg_steps[user_id] = {'step': 'giving_rating'}

@bot.message_handler(func=lambda msg: reg_steps.get(msg.from_user.id, {}).get('step') == 'giving_rating')
def feedback_finish(message):
    user_id = message.from_user.id
    rating_val = message.text
    del reg_steps[user_id]
    
    bot.send_message(user_id, "❤️ အကြံပြု သုံးသပ်ချက် ပေးပို့ခြင်းအတွက် ကျေးဇူးအများကြီးတင်ပါတယ်ဗျာ!")
    # Admin ဆီသို့ Feedback လှမ်းပို့ခြင်း
    bot.send_message(ADMIN_ID, f"📊 **Feedback အသစ်ရရှိသည်!**\nUser: {message.from_user.first_name} (ID: {user_id})\nRatingပေးချက်: {rating_val}")
    show_main_menu(user_id)

# --- 📊 ADMIN VIEW USERS COMMAND ---
@bot.message_handler(commands=['viewusers'])
def view_users(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.send_message(user_id, "❌ မင်းက Admin မဟုတ်လို့ ဒီ Command ကို သုံးခွင့်မရှိပါဘူး။")
        return
        
    total_users = len(users_db)
    bot.send_message(ADMIN_ID, f"📊 **စုစုပေါင်း User အရေအတွက်:** {total_users} ဦး\nစာရင်းများကို တစ်ပုံချင်းစီ ပို့ပေးနေပါတယ်...")
    
    for uid, udata in users_db.items():
        info_text = (
            f"🆔 TG ID: {uid}\n"
            f"📝 နာမည်/အသက်: {udata['name_age']}\n"
            f"🚻 အမျိုးအစား: {udata['gender']}\n"
            f"🎯 Preference: {udata['preference']}\n"
            f"💼 အလုပ်/စရိုက်: {udata['occupation']}\n"
            f"📍 တည်နေရာ: {udata['location_text']}"
        )
        bot.send_photo(ADMIN_ID, udata['photo'], caption=info_text)

# Bot ကို မောင်းနှင်ခြင်း
bot.infinity_polling()
