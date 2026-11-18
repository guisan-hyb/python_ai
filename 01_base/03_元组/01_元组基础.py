one_tuple = (1,)
print('one_tuple: ',one_tuple)
print('type(one_tuple): ',type(one_tuple))

user_tuple = ('小米','小红','20',30,40,True,False)
print('user_tuple: ',user_tuple)
print('type(user_tuple): ',type(user_tuple))

print(user_tuple[0])
print(user_tuple[1])
print(user_tuple[2])

for item in user_tuple:
    print(item)

print(user_tuple.index(True))
print(user_tuple.count('小米'))
print(len(user_tuple))
