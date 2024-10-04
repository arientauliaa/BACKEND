# CONTOH 1
def sambung_kata(**kwargs):
    print(kwargs)
    print(type(kwargs))
    
sambung_kata(a="Belajar", b="Python", c="di", d="STIKOM")

#CONTOH 2
def sambung_kata(**kata):
    for i in kata.values():
        print(i)
        
sambung_kata(a="Belajar", b="Python", c="di", d="STIKOM")
