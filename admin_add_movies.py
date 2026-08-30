"""
KINOLAR BAZASIGA QOSHISH SKRIPTI

Foydalanish:
1. CSV faylda kinolar ro'yxatini tayyorlash
2. Kinodan fayllarini 'kinolar/' papkasiga ko'chirish  
3. Skriptni ishga tushirish
"""

import sqlite3
import os
from pathlib import Path

DATABASE = 'kinolar.db'
KINOLAR_PAPKA = 'kinolar'

def init_db():
    """Bazani tekshirish va yaratish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kinolar (
            id INTEGER PRIMARY KEY,
            kod TEXT UNIQUE NOT NULL,
            nom TEXT NOT NULL,
            fayl_nomi TEXT NOT NULL,
            sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def csv_dan_qosh(csv_fayl):
    """CSV fayldan kinolar qo'shish
    Format: kod,nom,fayl_nomi
    Misol:
    101,Shuhrat,shuhrat.mp4
    102,Oybek,oybek.mp4
    """
    if not os.path.exists(csv_fayl):
        print(f"❌ Fayl topilmadi: {csv_fayl}")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    with open(csv_fayl, 'r', encoding='utf-8') as f:
        soni = 0
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):  # Sharhlar va bo'sh satrlarni o'tkazib yuborish
                continue
            
            parts = line.split(',')
            if len(parts) < 3:
                print(f"⚠️  Noto'g'ri format: {line}")
                continue
            
            kod = parts[0].strip()
            nom = parts[1].strip()
            fayl = parts[2].strip()
            
            # Fayl mavjudligini tekshirish
            fayl_path = f'{KINOLAR_PAPKA}/{fayl}'
            if not os.path.exists(fayl_path):
                print(f"⚠️  Fayl topilmadi: {fayl_path}")
                continue
            
            try:
                cursor.execute('''
                    INSERT INTO kinolar (kod, nom, fayl_nomi)
                    VALUES (?, ?, ?)
                ''', (kod, nom, fayl))
                soni += 1
                print(f"✅ {kod}: {nom}")
            except sqlite3.IntegrityError:
                print(f"⚠️  Kod allaqachon mavjud: {kod}")
            except Exception as e:
                print(f"❌ Xatolik ({kod}): {e}")
    
    conn.commit()
    conn.close()
    print(f"\n📊 Jami {soni} ta kino qo'shildi!")

def bir_kino_qosh(kod, nom, fayl_nomi):
    """Bitta kinodan qo'shish"""
    fayl_path = f'{KINOLAR_PAPKA}/{fayl_nomi}'
    
    if not os.path.exists(fayl_path):
        print(f"❌ Fayl topilmadi: {fayl_path}")
        return False
    
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
        print(f"❌ Kod allaqachon mavjud: {kod}")
        return False
    finally:
        conn.close()

def kinolarni_ko_rish():
    """Bazadagi barcha kinolarni ko'rish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT kod, nom, fayl_nomi FROM kinolar ORDER BY kod')
    kinolar = cursor.fetchall()
    conn.close()
    
    if not kinolar:
        print("📭 Kinolar bazasi bo'sh!")
        return
    
    print("\n" + "="*60)
    print(f"{'Kod':<10} {'Nomi':<30} {'Fayl':<20}")
    print("="*60)
    
    for kod, nom, fayl in kinolar:
        print(f"{kod:<10} {nom:<30} {fayl:<20}")
    
    print("="*60)
    print(f"📊 Jami: {len(kinolar)} ta kino\n")

def bazani_tozalash():
    """⚠️  FAQAT TEST UCHUN - Barcha kinolarni o'chirish"""
    javob = input("⚠️  DIQQAT! Barcha kinolar o'chiriladi. Tasdiqlaysizmi? (ha/yo'q): ")
    
    if javob.lower() in ['ha', 'yes', 'y']:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM kinolar')
        conn.commit()
        conn.close()
        print("✅ Baza tozalandi!")
    else:
        print("❌ Bekor qilindi")

# ============ MAIN MENU ============

if __name__ == '__main__':
    init_db()
    
    print("""
    🎬 KINOLAR BAZASINI BOSHQARISH
    ==============================
    
    1️⃣  CSV fayldan kinolar qo'shish
    2️⃣  Bitta kinodan qo'shish
    3️⃣  Bazadagi kinolarni ko'rish
    4️⃣  Bazani tozalash (O'CHIRISH)
    5️⃣  Chiqish
    """)
    
    while True:
        tanlov = input("\n👉 Tanlovingiz: ").strip()
        
        if tanlov == '1':
            csv = input("CSV fayl nomi (misol: kinolar.csv): ").strip()
            csv_dan_qosh(csv)
        
        elif tanlov == '2':
            kod = input("Kino kodi: ").strip()
            nom = input("Kino nomi: ").strip()
            fayl = input("Fayl nomi: ").strip()
            bir_kino_qosh(kod, nom, fayl)
        
        elif tanlov == '3':
            kinolarni_ko_rish()
        
        elif tanlov == '4':
            bazani_tozalash()
        
        elif tanlov == '5':
            print("👋 Shunovarida!")
            break
        
        else:
            print("❌ Noto'g'ri tanlov!")
