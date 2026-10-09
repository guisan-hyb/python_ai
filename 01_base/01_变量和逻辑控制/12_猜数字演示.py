import random

answer = random.randint(1,20)

while True:
    guess = int(input('输入: '))
    if guess == answer:
        print('right')
        break
    elif guess > answer:
        print('big')
    else:
        print(f'low')

