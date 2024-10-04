for i in range (1,11):
    print(i, 'x', i, '=', i*i)
    
for i in range (1,11):
    if i == 5:
        continue
    print(i, 'x', i, '=', i*i)
i = 0
while i < 10:
    i += 1
    if i == 5:
        continue
    print(i, 'x', i, '=', i*i)