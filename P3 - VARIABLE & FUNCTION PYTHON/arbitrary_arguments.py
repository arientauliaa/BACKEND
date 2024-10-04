# CONTOH 1 (ERROR)
def sapa_teman(nama1, nama2, nama3):
    print("Halo", nama1)
    print("Halo", nama2)
    print("Halo", nama3)
sapa_teman("Alex", "Nisa", "Sari")

# CONTOH 2
def sapa_teman(*args):
    print(args)
    print(type(args))
    
sapa_teman("Alex", "Nisa", "Sari", "Risa", "Arin", "Jua")