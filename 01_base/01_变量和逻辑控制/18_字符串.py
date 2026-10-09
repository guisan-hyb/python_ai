from itertools import count

from sphinx.search import pt

student_name1 = '小平'
student_name2 = '也帅'
print(student_name1,student_name2)
print(f'{type(student_name1)}, {type(student_name2)}')


str1 = '''
I love python
And you?
'''

str2 = """
I love python3
And you?
"""

print(str1,str2)
print(type(str1),type(str2))


msg = "It's a wonderful day"
print(msg)

msg = 'It\'s a wonderful day'
print(msg)

msg = 'He said "It\'s a great day"'
print(msg)

msg = "He said \"It's a great day\""
print(msg)


corse = 'python'
print(corse)
print(corse[0],corse[2],end=corse[3])
print()

'''
演示切片操作
序列[start:end:step]
start表示开始的索引，end表示结束的索引，[start,end)左闭右开
1. 索引是从0开始的
2. 正索引从左到右，依次增加，0，1，2，3，4...
3. 负索引从右到左，绝对值依次增加，-1,-2,-3,-4,-5...
4. 步长正数就是从左向右，如果是负数就是从右向左
start可以省略，如果省略，并且step为正数，start就是从下标0开始
如果step为负数，start就是从下标-1开始
end可以省略，如果省略，并且step为正数，end就是最后一个元素的下标的下一个位置
如果step为负数，end就是第一个元素的前一个位置，所以也可以取到第一个元素。
step也可以省略，默认步长为1
'''

digits = '0123456789'
print(digits[2:5:1])
print(digits[:5])
print(digits[2:])
print(digits[:])
print(digits[0::1])
print(digits[::2])
print(digits[::-1])
print(digits[-5:-1])
print(digits[0:-1])


'''
案例2：给定一个图片的名称为"photo.jpg"，代码实现获取这个图片的名称(photo)以及这个图片的后缀(.jpg)。

分析：

  * ① 建议先获取点号的位置（目前还未学习，只能一个一个数）
  * ② 从开头切片到点号位置，得到的就是文件的名称
  * ③ 从点号开始切片，一直到文件的结尾，则得到的就是文件的后缀
'''
index = 5
str = 'photo.jpg'
name = str[:5]
suffix = str[5:]
print(f'文件名: {name}, 后缀名: {suffix}')



'''
字符串查找
索引 = 字符串.find(子串)
如果字符串中包含子串，则find返回子串在字符串中的位置(索引)
如果字符串中不包含子串，则find返回-1

索引 = 字符串.index(子串)
如果字符串中包含子串，则index返回子串在字符串中的位置(索引)
如果字符串中不包含子串，则index抛出异常，程序崩溃

'''
message = 'welcome to Python programming, Python is good'
sub_str = 'Pythons'
position = message.find(sub_str)
if position == -1:
    print('not')
else:
    print(position)

'''
input输入一个文件名称，求.的索引下标
'''
# file_name = input('请输入文件名: ')
# dot_pos = file_name.find('.')
# if dot_pos == -1:
#     print('未找到., 文件格式有误')
# else:
#     print(f'找到.的位置{dot_pos}')
#     print(f'文件名: {file_name[:dot_pos]}')
#     print(f'后缀名: {file_name[dot_pos:]}')


fruits = 'apple, banana, orange'
pos = fruits.index('apple')
print(f'apple的位置: {pos}')

pos = fruits.index('orange')
print(f'orange位置: {pos}')

# 找不到会抛出异常，ValueError
# pos = fruits.index('oranges')
# print(f'orange的位置: {pos}')


'''
字符串替换
1. 替换后的全部字符串 = 原来的字符串.replace(要替换的原子串,替换后的子串,替换的次数)
替换次数如果不传递，那么就全部替换
原来的字符串不会被修改，只是会返回一个新的修改后的字符串
'''

text = 'I love Cpp programming and Cpp is powerful'
new_text = text.replace('Cpp','Python')
print(new_text)

new_text1 = text.replace('Cpp','Python',1)
print(new_text1)

new_text2 = text.replace('and','&&')
print(new_text2)


'''
字符串切割
列表 = 字符串.split(分隔符)
列表里存储的就是字符串按照分割符切割后的多个子串。
'''
data_str = '2024-03-14'
data_list = data_str.split('-')
print(data_list)

email = 'user@example.com'
parts = email.split('@')
print(f'用户名为: {parts[0]}')
print(f'邮箱: {parts[1]}')



'''
拼接后的字符串 = 连接符.join(列表)
将列表中的每个元素按照连接符进行拼接，最后汇总为一个拼接后的字符串
'''
fruits = ['apple','banana','orange']
result = '-'.join(fruits)
print(result)

words = ['Hello','Python','World']
words = '.'.join(words)
print(words)



'''
案例需求
生成一个6位随机验证码，要求包含大写字母、小写字母和数字的组合。
思路:
1. 将所有的大写字母，小写字母，数字序列都拼成一个完整的字符串
2. 进行随机抽取，从完整的字符串中随机抽取一个字符
random.randint(开始数字，结束的数字) 可以从开始的数字到结束的数字之间随机抽取一个数字
范围为[开始数字，结束数字]
可以利用上面的函数随机出一个索引，再根据索引获取字符即可
3. 将字符拼接成结果字符串
'''
import random
length = 6
codestr = ''

uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowwercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

all_charts = uppercase+lowwercase+digits

total_len = len(all_charts)

rand_idx = random.randint(0,total_len-1)
print(f'random index: {rand_idx}')
print(f'rand_char: {all_charts[rand_idx]}')

for i in range(6):
    rand_idx = random.randint(0,total_len-1)
    print(f'rand_idx: {rand_idx}')
    print(f'rand_char: {all_charts[rand_idx]}')
    codestr+=all_charts[rand_idx]

print(f'验证码: {codestr}')

