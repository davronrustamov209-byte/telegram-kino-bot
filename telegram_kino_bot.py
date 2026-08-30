import telebot
import sqlite3
import os
from dotenv import load_dotenv
from pathlib import Path

# .env faylidan token yuklash
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
DATABASE = 'kinolar.db'

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
            sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Foydalanuvchilar jadval (ixtiyoriy - statistika uchun)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foydalanuvchilar (
            user_id INTEGER PRIMARY KEY,
            ismi TEXT,
            kodlar_soni INTEGER DEFAULT 0,
            birinchi_marta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    
    # Statistika saqlash
    foydalanuvchi_malumot_saqlash(user_id, user_name)
    
    javob = f"""
🎬 Assalomu alaykum {user_name}, xush kelibsiz!

🎥 Kino kodini yozing va men uni sizga yuborib beraman.

Masalan: 102
    """
    bot.reply_to(message, javob)

@bot.message_handler(commands=['help'])
def help_command(message):
    """Yordam buyrug'i"""
    javob = """
📖 BOT QOLLASH:

1️⃣ Kino kodini yozing (masalan: 102)
2️⃣ Bot avtomatik tarzda kinoni yuboradi

📊 Boshqa buyruqlar:
/start - Botni qayta boshlash
/help - Bu xabar
/toplamli - Barcha kinolarni ko'rish (bosh admin uchun)
    """
    bot.reply_to(message, javob)

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
    
    # Statistika saqlash
    foydalanuvchi_malumot_saqlash(user_id, user_name)
    
    # Koddan kinodan topish
    kino = kino_topish(kod)
    
    if not kino:
        bot.reply_to(message, f"❌ {kod} kodli kino topilmadi!\n💡 Tog'ri kodni tekshiring.")
        return
    
    # Kinodan ma'lumotlar
    kino_id, kino_kod, kino_nom, fayl_nomi, sana = kino
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
                caption=f"🎬 {kino_nom}\n📌 Kod: {kino_kod}",
                supports_streaming=True
            )
        
        # Status xabarini o'chirish
        bot.delete_message(user_id, status_msg.message_id)
        
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
