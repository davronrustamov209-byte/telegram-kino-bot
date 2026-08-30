# 🎬 Telegram Kino Bot

Instagram Reels-dan kinolarni Telegram bot orqali yuborish tizimi.

## 📋 Tizim Tavsifi

```
Instagram Reels (30 soniya)
         ↓
    Kino kodi ko'rish
         ↓
    Bot linkini bosish
         ↓
Bot: "Kino kodini yozing"
         ↓
    Kod yozish (masalan: 102)
         ↓
Bot: Kinodan avtomatik yuborish ✅
```

---

## 🚀 O'RNATISH

### 1. Python Kutubxonalarini O'rnatish

```bash
# Requirements faylini yaratish (ixtiyoriy)
pip install pyTelegramBotAPI
pip install python-dotenv

# YOKI bir vaqtada:
pip install -r requirements.txt
```

### 2. Telegram Bot Token Olish

1. **Telegram-da** `@BotFather` ga xabar yuboring
2. `/newbot` buyrug'ini yozing
3. Bot nomini kiritish (masalan: `MyKinoBot`)
4. Username kiritish (masalan: `my_kino_bot`)
5. Token olasiz: `123456789:ABCDefGHIjKLmnOPqrSTuvWXYZ123456789`

### 3. .env Faylni Sozlash

`.env` faylni o'chiring va token qo'yish:

```
BOT_TOKEN=123456789:ABCDefGHIjKLmnOPqrSTuvWXYZ123456789
ADMIN_ID=987654321
```

**ADMIN_ID** topish:
- `/start` buyrug'ini botga yuboring
- @userinfobot ga link jo'nating
- Chiqadigan `ID` raqamni copy qiling

### 4. Kinolar Papkasini Yaratish

```bash
mkdir kinolar
# Kinodan MP4 fayllarini shu papkaga ko'chirish
# Masalan: kinolar/shuhrat.mp4
```

### 5. Kinolar Kodlarini Qo'shish

**Variant A: CSV fayldan**
```bash
# kinolar.csv faylni tayyorlang:
python admin_add_movies.py
# Tanlov: 1 (CSV fayldan qo'shish)
# kinolar.csv yozing
```

**Variant B: Qo'lda**
```bash
python admin_add_movies.py
# Tanlov: 2 (Bitta kinodan qo'shish)
```

**Kinolar ro'yxatini ko'rish:**
```bash
python admin_add_movies.py
# Tanlov: 3
```

---

## ▶️ BOTNI ISHGA TUSHIRISH

```bash
python telegram_kino_bot.py
```

**Konsol chiqarish:**
```
🤖 Bot ishga tushdi...
⏸  Toxtatish uchun: Ctrl + C
```

---

## 📱 FOYDALANUVCHI JARYONI

### Telegram-da

1. **Bot linki** (Instagram Reels-da yozilgan):
   ```
   t.me/your_bot_username?start
   ```

2. **Bot jarayoni:**
   ```
   User: /start
   Bot: "Assalomu alaykum! Kino kodini yozing"
   
   User: 102
   Bot: ⏳ "Oybek" yuborilmoqda...
   Bot: 🎥 [VIDEO FILE]
   Bot: ✅ "Oybek" muvaffaqiyatli yuborildi!
   ```

### Bot Buyruqlari

| Buyruq | Tavsifi |
|--------|---------|
| `/start` | Botni boshlash |
| `/help` | Yordam |
| `/toplamli` | Barcha kinolar (ADMIN) |
| `kodini yozish` | Kinodan yuborish |

---

## 🗂️ FAYL TUZILISHI

```
project/
├── telegram_kino_bot.py      # Asosiy bot kodi
├── admin_add_movies.py       # Kinolar qo'shish
├── .env                      # Token va sozlamalar
├── kinolar.csv              # Kinolar ro'yxati
├── kinolar/                 # Kinodan fayllar
│   ├── shuhrat.mp4
│   ├── oybek.mp4
│   └── ...
├── kinolar.db               # SQLite baza (avtomatik)
└── README.md                # Bu fayl
```

---

## ⚙️ SOZLAMALAR

### Fayl Hajmi

Telegram 2 GB gacha video yuboradi. Katta fayllar uchun:

```python
# telegram_kino_bot.py da tekshiring:
supports_streaming=True  # Oqim rejimida yuborish
```

### Tezlik

- Yuborish vaqti: Fayl hajmiga bog'liq (internet tezligiga)
- Bot javob vaqti: 1-2 soniya

### Xavfsizlik

1. **Token xavfsizligi:**
   - `.env` faylni `.gitignore` ga qo'yish
   - Token-ni hech kimga bermaslik

2. **Admin huquqlari:**
   ```python
   ADMIN_ID = 987654321  # Faqat o'zingizning ID
   ```

---

## 🐛 MUAMMOLAR VA YECHIM

### Muammo: "❌ ModuleNotFoundError: No module named 'telebot'"

**Yechim:**
```bash
pip install pyTelegramBotAPI
```

### Muammo: "❌ Faylni topa olmadim"

**Tekshiring:**
- Fayl `kinolar/` papkasida bor mi?
- Fayl nomi CSV-da to'g'ri yozilgan mi?

### Muammo: "❌ Bot javob bermaydi"

**Tekshiring:**
1. Token to'g'ri mi? (`.env`)
2. Bot internet bilan bog'langan mi?
3. `python telegram_kino_bot.py` ishga tushti mi?

### Muammo: Katta fayllar sekin yuboriladi

**Yechim:**
```python
# Video sifatini pasaytirish
# FFmpeg yordamida qayta kodlash:
ffmpeg -i original.mp4 -b:v 500k compressed.mp4
```

---

## 📊 STATISTIKA VA MONITORING

### Foydalanuvchilar Statistikasi

```bash
python admin_add_movies.py
# Keyin: SELECT * FROM foydalanuvchilar;
```

### Database Tekshirish

```python
# Python consolida:
import sqlite3
conn = sqlite3.connect('kinolar.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM kinolar')
print(cursor.fetchone())  # Jami kinolar soni
```

---

## 🔄 INSTAGRAM INTEGRATSIYASI

### Reels Yuborish Jaryoni

1. **30 soniya Reel tayyorlash:**
   - Editing app (TikTok, CapCut, Adobe Premiere)
   - Qiziqarli joyni qilib save qilish

2. **Kino kodini qo'yish:**
   - Reel caption-da: "Kodi: 102"
   - Reel ko'rinishdagi text: Kino kodi yozish

3. **Bot link qo'yish:**
   - Bio-da yoki Reel-da: `t.me/your_bot_username?start`

**Namuna Caption:**
```
🎬 Oybek kinosindan eng qiziq joylar!

🤖 Kinodan ko'rish uchun:
👉 @your_bot_username ga "102" yozing

#Kino #Oybek #TelegramBot
```

---

## 📈 KELECHI YAXSHILANISHLAR

```python
# Qo'shimcha funksiyalar qo'shish mumkin:

1. ❤️ Like/Dislike sistema
2. 💬 Sharhlar va o'chiqqalar
3. 🔎 Kino qidirish (nomi bo'yicha)
4. ⭐ Eng ko'p o'qilganlar
5. 📥 Izoh olish uchun forma
6. 📢 Yangi kino xabarlari
7. 🎁 Mukofot va bonus sistem
```

---

## 📞 YORDAM

**Muammo bo'lsa:**
1. README-ni qayta o'qish
2. `.env` faylni tekshirish
3. Console xatoliklarini o'qish
4. Fayl yo'llarini tekshirish

---

## 📝 LITSENZIYA

Bu kod bepul foydalanish uchun.

---

**Yaratildi:** 2024  
**Til:** Python 3.8+  
**Version:** 1.0
