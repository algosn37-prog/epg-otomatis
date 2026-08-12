import requests
from bs4 import BeautifulSoup
import datetime

# 1. Persiapan awal format XMLTV
xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="EPG TVRI tivie.id">
  <channel id="tvri.id">
    <display-name>TVRI Nasional</display-name>
  </channel>
"""

# 2. URL Target (TVRI di tivie.id)
url_target = "https://tivie.id/channel/tvri"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

try:
    print(f"Mencoba mengunduh jadwal dari {url_target}...")
    response = requests.get(url_target, headers=headers)
    response.raise_for_status() 
    
    # 3. Membedah HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Mencari semua elemen yang memiliki teks "WIB" (karena tivie.id selalu menggunakan penanda WIB untuk jamnya)
    waktu_elements = soup.find_all(string=lambda text: text and "WIB" in text)
    
    tanggal_hari_ini = datetime.datetime.now().strftime("%Y%m%d")
    
    for waktu_elem in waktu_elements:
        try:
            # Mengambil jam, contoh: "00:00 WIB" menjadi "00:00"
            jam_mentah = waktu_elem.strip()
            jam = jam_mentah.replace(" WIB", "").strip()
            
            # Memformat jam dengan membuang titik dua, contoh "00:00" -> "000000"
            jam_bersih = jam.replace(":", "") + "00"
            start_time = f"{tanggal_hari_ini}{jam_bersih} +0700"
            
            # Di struktur tivie.id, judul acara biasanya berada di elemen sebelahnya/setelahnya
            # Kita naik ke 'parent' (elemen pembungkusnya), lalu mencari elemen teks di sebelahnya
            parent_div = waktu_elem.find_parent()
            
            # Mencari judul acara di elemen saudaranya (sibling) atau div berikutnya
            judul_acara = "Acara Tidak Diketahui"
            
            # Logika pencarian judul khusus untuk tivie.id
            if parent_div and parent_div.find_next_sibling():
                judul_acara = parent_div.find_next_sibling().text.strip()
            elif parent_div and parent_div.parent:
                # Alternatif jika terbungkus dalam div yang sama
                semua_teks = parent_div.parent.text.strip()
                # Menghapus jam dari teks keseluruhan untuk mendapatkan judul
                judul_acara = semua_teks.replace(jam_mentah, "").strip()
            
            # Membersihkan spasi berlebih
            judul_acara = " ".join(judul_acara.split())
            
            # Memasukkan ke dalam XML
            xml_content += f"""
  <programme start="{start_time}" stop="" channel="tvri.id">
    <title>{judul_acara}</title>
  </programme>"""
  
        except Exception as e:
            print(f"Melewati satu acara karena eror pemformatan: {e}")
            continue

except Exception as e:
    print(f"Terjadi kesalahan saat mengambil data jaringan: {e}")

# 4. Menutup tag XML
xml_content += "\n</tv>"

# 5. Menyimpan hasil ke dalam file epg.xml
with open("epg.xml", "w", encoding="utf-8") as file:
    file.write(xml_content)
    
print("Berhasil mengambil data TVRI dari tivie.id dan memperbarui file epg.xml!")
