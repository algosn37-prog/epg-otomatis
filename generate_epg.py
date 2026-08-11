import datetime

# Catatan: Ini adalah skrip dasar. Untuk versi tingkat lanjut, 
# Anda akan menggunakan library 'requests' untuk menarik data dari web TV.

# Mengambil waktu hari ini
waktu_sekarang = datetime.datetime.now().strftime("%Y%m%d%H%M%S +0700")

xml_content = f"""

  
    TV Nasional
  
  
  
    Siaran Langsung Hari Ini
    File EPG ini diperbarui otomatis oleh robot GitHub Actions.
  

"""

# Menyimpan hasil ke dalam file epg.xml
with open("epg.xml", "w", encoding="utf-8") as file:
    file.write(xml_content)
    
print("Berhasil membuat file epg.xml yang baru!")
