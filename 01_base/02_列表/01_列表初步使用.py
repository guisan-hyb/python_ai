fruits = ['orange','apple','mange']
print(fruits)
print(type(fruits))

my_list = ['apple',123,True]
print(my_list)
print(type(my_list))

print(fruits[0])
print(fruits[1])
print(fruits[2])
print(fruits[-1])

print('-'*20)
for name in fruits:
    print(name)

print('-'*20)
index = 0
while index < len(fruits):
    print(fruits[index])
    index+=1

