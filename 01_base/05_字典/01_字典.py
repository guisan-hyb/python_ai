'''
定义字典
格式1  变量名称 = {key1:value1, key2:value2, ...}
格式2  变量名称2 = {} 空字典,
格式3  变量名称3 = dict()
'''
from sphinx.search import pt

person = {'name':'小明',
          'age':19,
          'address':'m78',
          'sex':'男',
          'hobby': 'game'}

print(person)
print(type(person))


dict1 = {}
print(type(dict1))
print(dict1)

dict2 = ()
print(type(dict2))
print(dict2)

print('*'*50)

for key in person:
    print(key)
    print(person[key])

person['salary'] = 35000
print(person)

person['age'] = 24
print(person)

del person['salary']
print(person)

person.clear()
print(person)
person = {'name':'a',
          'age':19,
          'address':'67cantin',
          'sex':'man',
          'hobby':'6767676'}
print(person.keys())

for key in person.keys():
    print(key)

print('x'*20)


print(person.items())
for item in person.items():
    print(item)
    print(item[0])
    print(item[1])
    print('?'*30)
    key,value = item
    print(key)
    print(value)
print('*',20)

for key,value in person.items():
    print(key)
    print(value)




'''
###  案例需求

给定一个字符串my_string，现在要求统计每个字符出现的次数: 
形成结果: {'字符':出现次数,'字符2':次数}
例如: 'abcdecf' ==> {'a':1,'b':1,'c':2,'d':1,'e':1,'f':1}
思路:
最开始弄一个空字典，key为字符，value为出现的次数
1. 如果字符没有在字典中，将字符和次数1插入字典
2. 如果字符在字典中，将字符的次数+1
3. 最后遍历字典，打印每个字符出现的次数
'''

str = 'abcdecf'
count_dict = {}
for ch in str:
    if ch not in count_dict:
        count_dict[ch]=1
        continue
    count_dict[ch]+=1

for key,value in count_dict.items():
    print(f'{key}:{value}')

