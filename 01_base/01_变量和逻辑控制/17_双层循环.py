for row in range(1,10):
    for col in range(1,row+1):
        print(f'{row} * {col} = {row*col}',end = '\t')
    print()

print('#'*20)


for row in range(1,10):
    for col in range(1,row+1):
        print(f'{col} * {row} = {row*col}',end = '\t')
        if col == 4:
            break
    print()

print('#'*20)

