def hitung_gaji(nama, golongan, jam_kerja):
    upah_per_jam = {
        'A' : 5000,
        'B' : 7000,
        'C' : 8000,
        'D' : 10000
    } 
# Cek apakah golongan valid
    if golongan in upah_per_jam:
        upah = upah_per_jam[golongan]
    else:
        return f"Golongan {golongan} tidak ditemukan!"
    
# Hitung uang lembur jika ada
    if jam_kerja > 48:
        jam_lembur = jam_kerja - 48
        uang_lembur = jam_lembur * 4000
    else:
        uang_lembur = 0
    
# Hitung gaji total
    gaji_total = (jam_kerja * upah) + uang_lembur
    
    return f"Nama Karyawan: {nama}, Gaji Total Per Minggu : {gaji_total}"

# Input data karyawan
nama = input("Masukkan nama karyawan: ")
golongan = input("Masukkan golongan karyawan (A, B, C, D): ").upper()
jam_kerja = int(input("Masukkan jumlah jam kerja per minggu : "))

hasil = hitung_gaji(nama, golongan, jam_kerja)
print(hasil)

