num = 1
while num<=10:
    if num==3:
        print(f'num=={num}')
        break
    print(f'{num}')
    num+=1
print('结束')

print('#'*20)

num = 1
while num<=10:
    if num == 3:
        print(f'num=={num}')
        num+=1
        continue
    print(f'{num}')
    num+=1
print('结束')


print('#'*20)

while True:
    print('endless')

