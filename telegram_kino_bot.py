import telebot
import sqlite3
import os
from dotenv import load_dotenv
from pathlib import Path
import json

# .env faylidan token yuklash
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

bot = telebot.TeleBot(BOT_TOKEN)
DATABASE = 'kinolar.db'

# Majburiy obuna kanallari (ENDI DATABASE-DAN O'QILADI!)
REQUIRED_CHANNELS = []  # Empty - database-dan o'qiladi

# ============ DATABASE SOZLASH ============

def init_db():
    """Bazani yaratish va tablitsa qo'shish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Kinolar jadval
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kinolar (
            id INTEGER PRIMARY KEY,
            kod TEXT UNIQUE NOT NULL,
            nom TEXT NOT NULL,
            fayl_nomi TEXT NOT NULL,
            kategoriya TEXT DEFAULT 'Umumiy',
            sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Kategoriyalar jadval
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kategoriyalar (
            id INTEGER PRIMARY KEY,
            nomi TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Foydalanuvchilar jadval
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foydalanuvchilar (
            user_id INTEGER PRIMARY KEY,
            ismi TEXT,
            kodlar_soni INTEGER DEFAULT 0,
            birinchi_marta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Yuklangan kinolar (temp)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS yuklangan_kinolar (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            fayl_id TEXT,
            nom TEXT,
            sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ✨ YANGI! Majburiy obuna kanallari
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS obuna_kanallari (
            id INTEGER PRIMARY KEY,
            channel_name TEXT UNIQUE NOT NULL,
            sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def kino_qosh(kod, nom, fayl_nomi):
    """Kinodan bazaga qo'shish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO kinolar (kod, nom, fayl_nomi)
            VALUES (?, ?, ?)
        ''', (kod, nom, fayl_nomi))
        conn.commit()
        print(f"✅ Kino qo'shildi: {kod} - {nom}")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ Kino {kod} allaqachon mavjud!")
        return False
    finally:
        conn.close()

def kino_topish(kod):
    """Koddan kinodan bazaga topish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM kinolar WHERE kod = ?', (kod,))
    result = cursor.fetchone()
    conn.close()
    
    return result

def obunani_tekshir(user_id):
    """Foydalanuvchi majburiy kanallarga obuna qilganini tekshirish"""
    # Database-dan kanallarni o'qish
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT channel_name FROM obuna_kanallari')
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    # Agar kanal yo'q bo'lsa, hamma ruxsat
    if not channels:
        return True
    
    # Har bir kanalni tekshirish
    for channel in channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            # Agar obuna bo'lmasa
            if member.status == 'left' or member.status == 'kicked':
                return False
        except:
            return False
    return True

def obuna_xabari():
    """Majburiy obuna kanallari haqida xabar"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT channel_name FROM obuna_kanallari')
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not channels:
        return "Majburiy kanallar yo'q"
    
    channels_text = '\n'.join([f'👉 {ch}' for ch in channels])
    return f"""
❌ DIQQAT!

Bu botdan foydalanish uchun quyidagi kanallarga obuna bo'lish majburiy:

{channels_text}

Obuna bo'lgach, yana harakat qilib ko'ring.
"""

def kanal_qosh(channel_name):
    """Yangi kanal qo'shish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # @ bilan yozilmagansa qo'shish
    if not channel_name.startswith('@'):
        channel_name = '@' + channel_name
    
    try:
        cursor.execute('INSERT INTO obuna_kanallari (channel_name) VALUES (?)', (channel_name,))
        conn.commit()
        conn.close()
        return True, f"✅ Kanal qo'shildi: {channel_name}"
    except sqlite3.IntegrityError:
        conn.close()
        return False, f"⚠️ Kanal allaqachon mavjud: {channel_name}"
    except Exception as e:
        conn.close()
        return False, f"❌ Xatolik: {str(e)}"

def kanal_ochir(channel_name):
    """Kanalni o'chirish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # @ bilan yozilmagansa qo'shish
    if not channel_name.startswith('@'):
        channel_name = '@' + channel_name
    
    try:
        cursor.execute('DELETE FROM obuna_kanallari WHERE channel_name = ?', (channel_name,))
        conn.commit()
        
        if cursor.rowcount > 0:
            conn.close()
            return True, f"✅ Kanal o'chirildi: {channel_name}"
        else:
            conn.close()
            return False, f"⚠️ Kanal topilmadi: {channel_name}"
    except Exception as e:
        conn.close()
        return False, f"❌ Xatolik: {str(e)}"

def kanallarni_ko_rish():
    """Barcha kanallarni ko'rish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT channel_name FROM obuna_kanallari ORDER BY sana DESC')
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return channels

def kategoriya_qosh(nomi):
    """Yangi kategoriya qo'shish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO kategoriyalar (nomi) VALUES (?)', (nomi,))
        conn.commit()
        print(f"✅ Kategoriya qo'shildi: {nomi}")
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ Kategoriya allaqachon mavjud: {nomi}")
        return False
    finally:
        conn.close()

def kategoriyalarni_ko_rish():
    """Barcha kategoriyalarni ko'rish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT nomi FROM kategoriyalar')
    cats = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return cats

def foydalanuvchi_malumot_saqlash(user_id, user_name):
    """Foydalanuvchi statistikasi saqlash"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO foydalanuvchilar (user_id, ismi)
        VALUES (?, ?)
    ''', (user_id, user_name))
    
    cursor.execute('''
        UPDATE foydalanuvchilar SET kodlar_soni = kodlar_soni + 1
        WHERE user_id = ?
    ''', (user_id,))
    
    conn.commit()
    conn.close()

# ============ BOT BUYRUQLARI ============

@bot.message_handler(commands=['start'])
def start(message):
    """Bot startlanganda"""
    user_name = message.from_user.first_name or "Foydalanuvchi"
    user_id = message.chat.id
    
    # Obunani tekshirish
    if not obunani_tekshir(user_id):
        bot.send_message(user_id, obuna_xabari())
        return
    
    # Statistika saqlash
    foydalanuvchi_malumot_saqlash(user_id, user_name)
    
    javob = f"""
🎬 Assalomu alaykum {user_name}, xush kelibsiz!

🎥 Kino kodini yozing va men uni sizga yuborib beraman.

Masalan: 102

📂 Kategoriyalar:
/kategoriyalar - Barcha kinolar

🔐 Admin:
/upload - Kino yuklash (ADMIN)
    """
    bot.send_message(user_id, javob)

@bot.message_handler(commands=['help'])
def help_command(message):
    """Yordam buyrug'i"""
    if message.from_user.id == ADMIN_ID:
        # Admin uchun extended help
        javob = """
📖 BOT QOLLASH (ADMIN):

🎬 FOYDALANUVCHILAR UCHUN:
/start - Botni boshlash
/kategoriyalar - Kinolarni turkumlar bo'yicha ko'rish

🎥 ADMIN - KINO BOSHQARISH:
/upload - Kinodan yuklaydigan qilib qo'yish
/toplamli - Barcha kinolar ro'yxati

📻 ADMIN - OBUNA KANALLAR:
/addchannel @name - Yangi kanal qo'shish
/removechannel @name - Kanal o'chirish
/channels - Barcha kanallarni ko'rish

MISOL:
/addchannel @my_channel
/removechannel @old_channel
        """
    else:
        # Oddiy foydalanuvchi uchun
        javob = """
📖 BOT QOLLASH:

1️⃣ Kino kodini yozing (masalan: 102)
2️⃣ Bot avtomatik tarzda kinoni yuboradi

📂 Kategoriyalar:
/kategoriyalar - Kinolarni turkumlar bo'yicha ko'rish

📌 Kino kodini qanday bilish?
Instagram Reels-dan kino kodini ko'ring!

/start - Botni qayta boshlash
        """
    
    bot.send_message(message.chat.id, javob)

@bot.message_handler(commands=['upload'])
def upload_start(message):
    """Admin kino yuklash"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Sizda bu buyruq uchun huquq yo'q!")
        return
    
    msg = bot.send_message(message.chat.id, "🎬 Kino nomi yozing:")
    bot.register_next_step_handler(msg, upload_get_name)

def upload_get_name(message):
    """Kino nomini olish"""
    kino_nom = message.text.strip()
    msg = bot.send_message(message.chat.id, "📌 Kino kodini yozing:")
    bot.register_next_step_handler(msg, upload_get_code, kino_nom)

def upload_get_code(message, kino_nom):
    """Kino kodini olish"""
    kino_kod = message.text.strip()
    msg = bot.send_message(message.chat.id, """
📂 Kategoriya tanlang:

1️⃣ Drama
2️⃣ Komediya
3️⃣ Aksyon
4️⃣ Boshqa

Raqamni yozing:
    """)
    bot.register_next_step_handler(msg, upload_get_category, kino_nom, kino_kod)

def upload_get_category(message, kino_nom, kino_kod):
    """Kategoriya olish"""
    tanlov = message.text.strip()
    
    kategoriyalar = {
        '1': 'Drama',
        '2': 'Komediya',
        '3': 'Aksyon',
        '4': 'Boshqa'
    }
    
    kategoriya = kategoriyalar.get(tanlov, 'Boshqa')
    
    msg = bot.send_message(message.chat.id, """
🎥 Endi videoni yuboring:

Video fayl yuklang:
    """)
    bot.register_next_step_handler(msg, upload_get_video, kino_nom, kino_kod, kategoriya)

def upload_get_video(message, kino_nom, kino_kod, kategoriya):
    """Video faylini olish"""
    try:
        if message.video:
            file_id = message.video.file_id
            file_info = bot.get_file(file_id)
            
            # Fayl saqlab qo'yish
            downloaded_file = bot.download_file(file_info.file_path)
            
            fayl_nomi = f"{kino_kod}_{kino_nom}.mp4"
            
            # kinolar papkasi yaratish
            if not os.path.exists('kinolar'):
                os.makedirs('kinolar')
            
            with open(f'kinolar/{fayl_nomi}', 'wb') as f:
                f.write(downloaded_file)
            
            # Database-ga qo'shish
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO kinolar (kod, nom, fayl_nomi, kategoriya)
                VALUES (?, ?, ?, ?)
            ''', (kino_kod, kino_nom, fayl_nomi, kategoriya))
            
            conn.commit()
            conn.close()
            
            bot.send_message(message.chat.id, f"""
✅ Kino muvaffaqiyatli yuklandi!

📌 Kod: {kino_kod}
🎬 Nom: {kino_nom}
📂 Kategoriya: {kategoriya}
            """)
        else:
            bot.reply_to(message, "❌ Video fayli yuborish kerak!")
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {str(e)}")

@bot.message_handler(commands=['kategoriyalar'])
def show_categories(message):
    """Kategoriyalarni ko'rish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT kategoriya FROM kinolar ORDER BY kategoriya')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not categories:
        bot.reply_to(message, "📭 Kategoriyalar bo'sh!")
        return
    
    javob = "📂 KATEGORIYALAR:\n\n"
    for i, cat in enumerate(categories, 1):
        javob += f"{i}️⃣ /{cat.lower().replace(' ', '_')} - {cat}\n"
    
    bot.send_message(message.chat.id, javob)

# ✨ YANGI! KANAL BOSHQARISH BUYRUQLARI

@bot.message_handler(commands=['addchannel'])
def add_channel(message):
    """Admin: Yangi obuna kanali qo'shish"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Sizda bu buyruq uchun huquq yo'q!")
        return
    
    # Buyruqdan kanal nomini olish: /addchannel @channel_name
    text = message.text.strip()
    parts = text.split()
    
    if len(parts) < 2:
        bot.reply_to(message, """
❌ Format xato!

To'g'ri format:
/addchannel @channel_name

Misol:
/addchannel @my_channel
/addchannel channel_name
        """)
        return
    
    channel_name = parts[1]
    success, msg = kanal_qosh(channel_name)
    
    bot.reply_to(message, msg)

@bot.message_handler(commands=['removechannel'])
def remove_channel(message):
    """Admin: Obuna kanalini o'chirish"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Sizda bu buyruq uchun huquq yo'q!")
        return
    
    # Buyruqdan kanal nomini olish: /removechannel @channel_name
    text = message.text.strip()
    parts = text.split()
    
    if len(parts) < 2:
        bot.reply_to(message, """
❌ Format xato!

To'g'ri format:
/removechannel @channel_name

Misol:
/removechannel @my_channel
        """)
        return
    
    channel_name = parts[1]
    success, msg = kanal_ochir(channel_name)
    
    bot.reply_to(message, msg)

@bot.message_handler(commands=['channels'])
def show_channels(message):
    """Admin: Barcha obuna kanallarini ko'rish"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Sizda bu buyruq uchun huquq yo'q!")
        return
    
    channels = kanallarni_ko_rish()
    
    if not channels:
        bot.reply_to(message, "📭 Majburiy obuna kanallari yo'q!")
        return
    
    javob = "📻 MAJBURIY OBUNA KANALLARI:\n\n"
    for i, ch in enumerate(channels, 1):
        javob += f"{i}️⃣ {ch}\n"
    
    bot.send_message(message.chat.id, javob)

@bot.message_handler(commands=['toplamli'])
def toplamli(message):
    """Admin: Barcha kinolar ro'yxati"""
    # SHUNDAY ADMIN ID BILAN TEKSHIRING
    ADMIN_ID = 123456789  # O'zingizning Telegram ID
    
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Sizda bu buyruq uchun huquq yo'q!")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT kod, nom FROM kinolar ORDER BY kod')
    kinolar = cursor.fetchall()
    conn.close()
    
    if not kinolar:
        bot.reply_to(message, "📭 Kinolar bazasi bo'sh!")
        return
    
    javob = "📽️ **BARCHA KINOLAR RO'YXATI:**\n\n"
    for kod, nom in kinolar:
        javob += f"🎯 {kod}: {nom}\n"
    
    bot.reply_to(message, javob)

@bot.message_handler(func=lambda message: True)
def kino_chiqarish(message):
    """Kino kodini olish va kinodan yuborish"""
    user_id = message.chat.id
    user_name = message.from_user.first_name or "Foydalanuvchi"
    kod = message.text.strip()
    
    # 🔐 OBUNANI TEKSHIRISH
    if not obunani_tekshir(user_id):
        bot.send_message(user_id, obuna_xabari())
        return
    
    # Statistika saqlash
    foydalanuvchi_malumot_saqlash(user_id, user_name)
    
    # Koddan kinodan topish
    kino = kino_topish(kod)
    
    if not kino:
        bot.reply_to(message, f"❌ {kod} kodli kino topilmadi!\n💡 Tog'ri kodni tekshiring.")
        return
    
    # Kinodan ma'lumotlar
    kino_id, kino_kod, kino_nom, fayl_nomi, kategoriya, sana = kino
    fayl_path = f'kinolar/{fayl_nomi}'
    
    # Fayl mavjudligini tekshiring
    if not os.path.exists(fayl_path):
        bot.reply_to(message, f"❌ Faylni topa olmadim: {fayl_nomi}")
        return
    
    # Kinodan yuborish
    try:
        # Buyuk fayllar uchun progress xabari
        status_msg = bot.send_message(user_id, f"⏳ {kino_nom} yuborilmoqda...")
        
        with open(fayl_path, 'rb') as video:
            bot.send_video(
                user_id,
                video,
                caption=f"🎬 {kino_nom}\n📌 Kod: {kino_kod}\n📂 Kategoriya: {kategoriya}",
                supports_streaming=True
            )
        
        # Status xabarini o'chirish
        try:
            bot.delete_message(user_id, status_msg.message_id)
        except:
            pass
        
        # Muvaffaqiyat xabari
        bot.send_message(user_id, f"✅ {kino_nom} muvaffaqiyatli yuborildi!")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {str(e)}")
        print(f"Xatolik: {e}")

# ============ ADMIN FUNKSIYALARI ============

def kino_qosh_batch(kinolar_csv):
    """CSV fayldan kinolar qo'shish
    Format: kod,nom,fayl_nomi
    """
    with open(kinolar_csv, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                kod, nom, fayl = line.strip().split(',')
                kino_qosh(kod.strip(), nom.strip(), fayl.strip())

# ============ BOT BOSHLASH ============

if __name__ == '__main__':
    init_db()
    print("🤖 Bot ishga tushdi...")
    print("⏸  Toxtatish uchun: Ctrl + C")
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n👋 Bot to'xtatildi")
