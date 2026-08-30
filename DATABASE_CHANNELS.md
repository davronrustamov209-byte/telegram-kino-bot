# 📻 DATABASE CHANNEL MANAGEMENT

**Majburiy obuna kanallarini bot ichidan boshqarish!**

---

## 🎯 NIMA?

Hozir siz **bot ichidan** kanallarni qo'sha/o'chira olasiz!

**ENDI KERAK EMAS:**
```
❌ Code tahrir qilish
❌ GitHub push qilish
❌ Railway redeploy qilish
```

**YANGI:**
```
✅ Bot command qo'shish: /addchannel @channel
✅ Bot command o'chirish: /removechannel @channel
✅ Bot command ko'rish: /channels
```

---

## 🚀 ADMIN COMMANDS

### 1️⃣ KANAL QO'SHISH

```
/addchannel @my_channel
```

**Javob:**
```
✅ Kanal qo'shildi: @my_channel
```

**Database-ga saqlandi:**
```sql
obuna_kanallari table-ga insert
channel_name: @my_channel
```

---

### 2️⃣ KANAL O'CHIRISH

```
/removechannel @old_channel
```

**Javob:**
```
✅ Kanal o'chirildi: @old_channel
```

---

### 3️⃣ BARCHA KANALLARNI KO'RISH

```
/channels
```

**Javob:**
```
📻 MAJBURIY OBUNA KANALLARI:

1️⃣ @channel1
2️⃣ @channel2
3️⃣ @channel3
```

---

## 🔄 FLOW - FOYDALANUVCHI

### Scenario 1: Obuna qilgan

```
User: /start
↓
Bot: obunani_tekshir() → Database-dan kanallarni o'qish
↓
Obuna qilganmi? → HA ✅
↓
Bot: "Assalomu alaykum! Kino kodini yozing"
↓
User: 101
↓
✅ Kino yuborildi!
```

### Scenario 2: Obuna qilmagan

```
User: /start
↓
Bot: obunani_tekshir() → Database-dan kanallarni o'qish
↓
Obuna qilganmi? → YO'Q ❌
↓
Bot: "❌ Bu kanallarga obuna bo'ling:
      @channel1
      @channel2
      @channel3"
↓
Obuna bo'lgach, /start yana bosish
```

---

## 📊 DATABASE STRUKTURA

### obuna_kanallari Table

```sql
CREATE TABLE obuna_kanallari (
    id INTEGER PRIMARY KEY,
    channel_name TEXT UNIQUE,     -- @channel1
    sana TIMESTAMP                -- Qo'shilgan vaqti
)
```

**Misol Data:**
```
id  | channel_name  | sana
1   | @channel1     | 2026-08-30 15:30:00
2   | @channel2     | 2026-08-30 15:32:00
3   | @channel3     | 2026-08-30 15:35:00
```

---

## 💻 CODE FLOW

### obunani_tekshir() Function

```python
def obunani_tekshir(user_id):
    # 1. Database-dan kanallarni o'qish
    cursor.execute('SELECT channel_name FROM obuna_kanallari')
    channels = [row[0] for row in cursor.fetchall()]
    
    # 2. Agar kanal yo'q bo'lsa, hamma ruxsat
    if not channels:
        return True
    
    # 3. Har bir kanalini tekshirish
    for channel in channels:
        member = bot.get_chat_member(channel, user_id)
        if member.status == 'left':
            return False  # Obuna bo'lmadi!
    
    return True  # Barcha kanallarga obuna!
```

### kanal_qosh() Function

```python
def kanal_qosh(channel_name):
    # @ bilan yozing bo'lmasa qo'shish
    if not channel_name.startswith('@'):
        channel_name = '@' + channel_name
    
    # Database-ga INSERT
    cursor.execute('''
        INSERT INTO obuna_kanallari (channel_name)
        VALUES (?)
    ''', (channel_name,))
    
    return True, f"✅ Kanal qo'shildi: {channel_name}"
```

---

## 🎯 ADMIN SETUP

### Step 1: Bot-ni Channel Admin qilish

**Har bir kanal-da:**

1. Channel → Members
2. Bot-ni add qilish
3. Bot-ni "Admin" qilish
4. Huquqlar: "Post messages" enable

---

### Step 2: Bot Commands Ishlatish

**Telegram-da:**

```
/addchannel @channel1
/addchannel @channel2
/addchannel @channel3

/channels  ← Barcha kanallarni ko'rish
```

---

## 🔒 SECURITY

✅ **ADMIN_ID tekshirish:**
```python
if message.from_user.id != ADMIN_ID:
    return "❌ Sizda huquq yo'q!"
```

✅ **Duplicate kanallar yo'q:**
```sql
channel_name TEXT UNIQUE  ← Bir marta qo'shish mumkin
```

✅ **Kanal validation:**
```python
try:
    member = bot.get_chat_member(channel, user_id)
except:
    return False  ← Kanal yo'q yoki bot yo'q
```

---

## 📋 EXAMPLES

### EXAMPLE 1: 3 Kanal Qo'shish

```
/addchannel @kino_updates
✅ Kanal qo'shildi: @kino_updates

/addchannel @movie_news
✅ Kanal qo'shildi: @movie_news

/addchannel @entertainment
✅ Kanal qo'shildi: @entertainment

/channels
📻 MAJBURIY OBUNA KANALLARI:
1️⃣ @kino_updates
2️⃣ @movie_news
3️⃣ @entertainment
```

### EXAMPLE 2: Kanal O'chirish

```
/removechannel @old_channel
✅ Kanal o'chirildi: @old_channel

/channels
📻 MAJBURIY OBUNA KANALLARI:
1️⃣ @kino_updates
2️⃣ @movie_news
```

### EXAMPLE 3: User Flow

```
User: /start
Bot: (Tekshirish) Obuna qilgan?
     @kino_updates, @movie_news, @entertainment

Agar YO'Q:
Bot: ❌ DIQQAT!
     Bu kanallarga obuna bo'ling:
     👉 @kino_updates
     👉 @movie_news
     👉 @entertainment

Agar HA:
Bot: ✅ Assalomu alaykum! 
     Kino kodini yozing.
```

---

## 🚨 ERRORS VA YECHIM

### Error: "Duplicate entry"

**Sababи:** Kanal allaqachon qo'shilgan

**Yechim:**
```
/removechannel @channel
/addchannel @channel
```

### Error: "Kanal topilmadi"

**Sababи:** `/removechannel @wrong_name`

**Yechim:** `/channels` bilan barcha kanallarni ko'rish

### Error: "Bot is not member"

**Sababu:** Bot kanalga add qilinmagan

**Yechim:** Bot-ni kanallarga add qilish va admin qilish

---

## 📱 TEST QILISH

### Local Test

```bash
# 1. Bot ishga tushirish
python telegram_kino_bot.py

# 2. Admin buyrug'i
/addchannel @test_channel

# 3. Database tekshirish
sqlite3 kinolar.db
SELECT * FROM obuna_kanallari;

# 4. User test
/start → Obuna tekshiriladi
```

### Railway Test

```
1. GitHub-ga upload
2. Railway redeploy
3. Telegram: /addchannel @channel
4. Telegram: /channels (tekshirish)
5. User: /start (obuna check)
```

---

## 🎊 ADVANTAGES

✅ **Hech code tahrir kerak emas** - Bot commands ishlatamiş!  
✅ **Hech redeploy kerak emas** - Database update!  
✅ **Hech manual ishlash kerak emas** - Avtomatik check!  
✅ **Istalgan vaqtda update qilish** - Runtime changes!

---

## 📊 DATABASE QUERIES

### Kanallarni ko'rish

```sql
SELECT * FROM obuna_kanallari;
```

### Kanalni o'chirish (manual)

```sql
DELETE FROM obuna_kanallari WHERE channel_name='@channel';
```

### Barcha kanallarni o'chirish

```sql
DELETE FROM obuna_kanallari;
```

---

## 🚀 SETUP SUMMARY

1. **GitHub-ga upload:** `telegram_kino_bot.py` (yangilangan)
2. **Railway redeploy**
3. **Bot-ni admin qilish:** Har bir kanallada
4. **Kanallarni qo'shish:** `/addchannel @channel1` (Telegram-da)
5. **Test qilish:** `/channels` (kanallarni ko'rish)

---

**TAYYOR! DATABASE CHANNEL MANAGEMENT!** 🎉
