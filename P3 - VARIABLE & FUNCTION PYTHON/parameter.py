# CONTOH 1
def tambah (var1 = 5, var2 = 2):
    return var1 + var2
print ( tambah())
print( tambah(1))
print ( tambah(1, 6))
print ( tambah(5, 4))

# CONTOH 2
def pangkat(angka, pangkat = 2):
    hasil = 1
    for i in range(0, pangkat):
        hasil = hasil * angka
    return hasil;

print(pangkat(3)) # hanya mengubah angka depan saja
print(pangkat(5))
print(pangkat(10))
print(pangkat(3, 3)) # angka dan pangkat diubah
print(pangkat(5, 4))
print(pangkat(6, 6 ))