"""
BOT STATISTIKASI VA TAHLILI
"""

import sqlite3
from datetime import datetime, timedelta
from collections import Counter

DATABASE = 'kinolar.db'

def get_stats():
    """Barcha statistika olish"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Jami kinolar soni
    cursor.execute('SELECT COUNT(*) FROM kinolar')
    jami_kinolar = cursor.fetchone()[0]
    
    # Jami foydalanuvchilar
    cursor.execute('SELECT COUNT(*) FROM foydalanuvchilar')
    jami_foydalanuvchilar = cursor.fetchone()[0]
    
    # Jami kodlar yozildi
    cursor.execute('SELECT SUM(kodlar_soni) FROM foydalanuvchilar')
    jami_kodlar = cursor.fetchone()[0] or 0
    
    # Eng ko'p oqilgan kinolar
    cursor.execute('''
        SELECT kod, nom FROM kinolar 
        ORDER BY kod DESC 
        LIMIT 10
    ''')
    kinolar = cursor.fetchall()
    
    # So'nggi qo'shilgan 5 kino
    cursor.execute('''
        SELECT kod, nom, sana FROM kinolar 
        ORDER BY sana DESC 
        LIMIT 5
    ''')
    yangi_kinolar = cursor.fetchall()
    
    conn.close()
    
    return {
        'jami_kinolar': jami_kinolar,
        'jami_foydalanuvchilar': jami_foydalanuvchilar,
        'jami_kodlar': jami_kodlar,
        'kinolar': kinolar,
        'yangi_kinolar': yangi_kinolar
    }

def print_stats():
    """Statistikani chop etish"""
    stats = get_stats()
    
    print("\n" + "="*50)
    print("📊 BOT STATISTIKASI")
    print("="*50)
    
    print(f"""
    🎬 Kinolar:           {stats['jami_kinolar']} ta
    👥 Foydalanuvchilar:  {stats['jami_foydalanuvchilar']} ta
    🔢 Kod so'rovi:       {stats['jami_kodlar']} marta
    """)
    
    print("\n📈 SO'NGGI QO'SHILGAN KINOLAR:")
    print("-" * 50)
    for kod, nom, sana in stats['yangi_kinolar']:
        print(f"  {kod}: {nom}")
        print(f"     Vaqti: {sana[:19]}")
    
    print("\n" + "="*50)

def export_csv():
    """Statistikani CSV ga yuklash"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Foydalanuvchilar statistikasi
    cursor.execute('''
        SELECT user_id, ismi, kodlar_soni, birinchi_marta 
        FROM foydalanuvchilar 
        ORDER BY kodlar_soni DESC
    ''')
    
    with open('statistika_foydalanuvchilar.csv', 'w', encoding='utf-8') as f:
        f.write("User ID,Ismi,Kodlar Soni,Qo'shilgan Vaqti\n")
        for row in cursor.fetchall():
            f.write(f"{row[0]},{row[1]},{row[2]},{row[3]}\n")
    
    print("✅ statistika_foydalanuvchilar.csv saqlandi")
    
    # Kinolar statistikasi
    cursor.execute('SELECT kod, nom, sana FROM kinolar ORDER BY kod')
    
    with open('statistika_kinolar.csv', 'w', encoding='utf-8') as f:
        f.write("Kod,Nomi,Qo'shilgan Vaqti\n")
        for row in cursor.fetchall():
            f.write(f"{row[0]},{row[1]},{row[2]}\n")
    
    print("✅ statistika_kinolar.csv saqlandi")
    conn.close()

def top_users():
    """Eng faol foydalanuvchilar"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT ismi, kodlar_soni, birinchi_marta 
        FROM foydalanuvchilar 
        ORDER BY kodlar_soni DESC 
        LIMIT 10
    ''')
    
    users = cursor.fetchall()
    conn.close()
    
    print("\n👥 ENG FAOL FOYDALANUVCHILAR (TOP 10):")
    print("-" * 50)
    
    for rank, (name, kodlar, vaqti) in enumerate(users, 1):
        print(f"{rank}. {name}: {kodlar} ta so'rov")
    
    print()

if __name__ == '__main__':
    while True:
        print("""
        📊 STATISTIKA MENYU
        ==================
        1. Statistikani ko'rish
        2. Eng faol foydalanuvchilar
        3. CSV ga yuklash
        4. Chiqish
        """)
        
        tanlov = input("👉 Tanlovingiz: ").strip()
        
        if tanlov == '1':
            print_stats()
        elif tanlov == '2':
            top_users()
        elif tanlov == '3':
            export_csv()
        elif tanlov == '4':
            print("👋 Shunovarida!")
            break
        else:
            print("❌ Noto'g'ri tanlov!")
