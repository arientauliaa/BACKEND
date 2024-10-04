# CONTOH 1
def harga_setelah_pajak(harga_dasar):
    return harga_dasar + (harga_dasar * 10/100)

harga_cilok = 5000
harga_final_cilok = harga_setelah_pajak (harga_cilok)
print("Harga cilok 1 porsi Rp.", harga_final_cilok)