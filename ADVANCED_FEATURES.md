# 🚀 ADVANCED BOT FEATURES

**3 Yangi Feature:**
1. 🎥 Admin kino upload
2. 📂 Kategoriyalar/Bolimlar  
3. 🔐 Majburiy obuna kanallari

---

## 1️⃣ ADMIN KINO UPLOAD

### Nima?
Admin telegram-dan **BEVOSITA** kinodan yuklab qo'yadi!

### Qanday?

```
/upload buyrug'ini bosing
↓
Kino nomi yozing (masalan: "Shuhrat")
↓
Kino kodini yozing (masalan: "101")
↓
Kategoriya tanlang (Drama, Komediya, va boshqalar)
↓
Video file-ni yuboring
↓
✅ Kino muvaffaqiyatli saqlandi!
```

### Code-da setup:

**telegram_kino_bot.py-da:**

```python
ADMIN_ID = 1775624359  # O'zingizning ID
```

### Flow:

```
/upload
    ↓
@bot.message_handler(commands=['upload'])
    ↓
upload_get_name (Nomi)
    ↓
upload_get_code (Kodi)
    ↓
upload_get_category (Kategoriya)
    ↓
upload_get_video (Video file)
    ↓
SQLite-ga INSERT + kinolar/ papkaga SAVE
```

---

## 2️⃣ KATEGORIYALAR/BOLIMLAR

### Nima?
Kinolarni turkumlarga bo'lish:
- 📽️ Drama
- 😂 Komediya  
- 💥 Aksyon
- 🎬 Boshqa

### Qanday?

```
/kategoriyalar - Barcha bolimlarni ko'rish

📂 KATEGORIYALAR:

1️⃣ /drama - Drama
2️⃣ /komediya - Komediya
3️⃣ /aksyon - Aksyon
4️⃣ /boshqa - Boshqa
```

### Kategoriya bo'yicha kinolarni ko'rish:

```python
@bot.message_handler(commands=['drama'])
def drama_films(message):
    # Faqat drama kinolari ko'rsin
```

### Database struktura:

```sql
kinolar table:
┌──┬───┬────────┬────────┬───────────┐
│id│kod│nom     │fayl    │kategoriya │
├──┼───┼────────┼────────┼───────────┤
│1 │101│Shuhrat │..mp4   │Drama      │
│2 │102│Oybek   │..mp4   │Komediya   │
└──┴───┴────────┴────────┴───────────┘
```

---

## 3️⃣ MAJBURIY OBUNA KANALLARI

### Nima?
Kino ko'rishdan oldin foydalanuvchi kanallarga obuna bo'lish majburiy!

### Setup:

**telegram_kino_bot.py-da channels o'zgartirish:**

```python
REQUIRED_CHANNELS = [
    '@channel1',
    '@channel2',
    '@channel3'
]
```

### Flow:

```
Foydalanuvchi: /start yoki kod yozdi
    ↓
Bot: obunani_tekshir(user_id)
    ↓
Obuna bo'lganmi?
    ├─ YO'Q → "Bu kanallarga obuna bo'ling" xabari
    │         @channel1, @channel2, @channel3
    │
    └─ HA → Kino yuborish
```

### Xabar Template:

```
❌ DIQQAT!

Bu botdan foydalanish uchun quyidagi kanallarga 
obuna bo'lish majburiy:

👉 @channel1
👉 @channel2
👉 @channel3

Obuna bo'lgach, yana harakat qilib ko'ring.
```

### Channels yaratish:

1. Telegram-da **yangi channel** yarating
2. Channel nomi: `@my_channel_name`
3. Private yoki Public tanlang
4. **Bot linkini** channel bio-da qo'ying

---

## 🔄 DATABASE TABLES

### kinolar
```sql
CREATE TABLE kinolar (
    id INTEGER PRIMARY KEY,
    kod TEXT UNIQUE,              -- 101, 102...
    nom TEXT,                     -- Kino nomi
    fayl_nomi TEXT,               -- shuhrat.mp4
    kategoriya TEXT DEFAULT 'Umumiy',  -- Drama, Komediya...
    sana TIMESTAMP
)
```

### kategoriyalar
```sql
CREATE TABLE kategoriyalar (
    id INTEGER PRIMARY KEY,
    nomi TEXT UNIQUE              -- Drama, Komediya...
)
```

### yuklangan_kinolar (temp)
```sql
CREATE TABLE yuklangan_kinolar (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    fayl_id TEXT,
    nom TEXT,
    sana TIMESTAMP
)
```

---

## 📋 ADMIN COMMANDS

| Buyruq | Tavsifi |
|--------|---------|
| `/upload` | Kino yuklaydigan qilib qo'yish |
| `/kategoriyalar` | Barcha bolimlarni ko'rish |
| `/toplamli` | Barcha kinolar ro'yxati |
| `/help` | Yordam |

---

## 💡 USAGE EXAMPLE

### Admin upload:

```
Admin: /upload
Bot: "Kino nomi yozing:"
Admin: "Shuhrat"
Bot: "Kino kodini yozing:"
Admin: "101"
Bot: "Kategoriya tanlang (1-4):"
Admin: "1"
Bot: "Endi videoni yuboring:"
Admin: [video file]
Bot: "✅ Kino muvaffaqiyatli yuklandi!"
```

### Foydalanuvchi kino ko'rish:

```
User: /start
Bot: (obuna tekshirildi)
      "Assalomu alaykum! Kino kodini yozing"

User: 101
Bot: (kino yuborildi - "Shuhrat")
     "✅ Muvaffaqiyatli yuborildi!"
```

### Obuna bo'lmagan foydalanuvchi:

```
User: 101
Bot: "❌ DIQQAT!
     Bu botdan foydalanish uchun quyidagi 
     kanallarga obuna bo'lish majburiy:
     
     👉 @channel1
     👉 @channel2
     
     Obuna bo'lgach, yana harakat qilib ko'ring."
```

---

## 🎯 SETUP QADAM-QADAM

### 1. REQUIRED_CHANNELS O'ZGARTIRISH

**telegram_kino_bot.py:**

```python
REQUIRED_CHANNELS = ['@your_channel1', '@your_channel2']
```

### 2. ADMIN_ID TEKSHIRISH

```python
ADMIN_ID = 1775624359  # O'zingizning ID
```

### 3. GITHUB-GA UPLOAD

1. `telegram_kino_bot.py` o'zgartilgan versiyasini upload
2. Commit: "Add advanced features: upload, categories, subscription"
3. Railway auto-redeploy

### 4. TEST QILISH

```
Admin: /upload
     ↓ Kino yuklash
     ↓
User: /start
     ↓ Obuna tekshiriladi
     ↓
User: kino_kod
     ↓ Kino yuboriladi ✅
```

---

## 🚨 ERRORS VA YECHIM

### Error: "Bot is not member of channel"

**Sabab:** Bot kanallarga admin qilib qo'yilmagan

**Yechim:** 
1. Bot-ni kanallarga admin qilib qo'ying
2. Bot-ga message yuborish huquqi bering

### Error: "Video file not found"

**Sabab:** kinolar/ papka yo'q yoki fayl yo'q

**Yechim:**
1. `kinolar/` papka yaratish
2. Video faylni shu yerga ko'chirish

### Error: "Admin ID not defined"

**Sabab:** `.env`-da ADMIN_ID yo'q

**Yechim:**
```
ADMIN_ID=1775624359
```

---

## 🎊 KEYING QADAM

1. **Channels yaratish** (3 ta)
2. **Bot-ni admin qilib qo'yish** (channels-da)
3. **Code update qilish** (REQUIRED_CHANNELS)
4. **GitHub upload**
5. **Railway redeploy**
6. **Admin test** (`/upload`)
7. **User test** (`/start` → obuna check)

---

**TAYYOR! 3 ADVANCED FEATURE!** 🚀
