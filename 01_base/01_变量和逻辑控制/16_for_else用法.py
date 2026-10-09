str = 'python'
for i in str:
    if i=='h':
        print('遇到h, 强制结束')
        break
    print(i)
else:
    print('循环正常结束后的其他逻辑')

print('#'*50)

str = 'python'
for i in str:
    if i == 'h':
        print('遇到h不打印')
        continue
    print(i)
else:
    print('循环正常结束执行此处代码')

print('#'*50)

for i in range(6):
    print(i)
else:
    print('循环正常结束')

print('#'*50)

