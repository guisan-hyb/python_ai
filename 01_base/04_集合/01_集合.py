'''
定义集合方式
方式1 空集合: empty_set = set()
方式2 包含元素的集合 my_set = {元素1, 元素}
'''

empty_set = set()
print(empty_set)
print(type(empty_set))

empty_dict = {}
print(empty_dict)
print(type(empty_dict))

name_set = {'a','b','c','d','d'}
print(name_set)
print(type(name_set))

for name in name_set:
    print(name)

name_set.add('e')
print(name_set)

name_set.remove('b')
print(name_set)

if 'a' in name_set:
    print('y')
else:
    print('n')

if 'd' not in name_set:
    print('n')
else:
    print('y')



"""
💡 题目：一个数组中除了两个数字只出现一次外，其他数字都出现两次。
       找出这两个只出现一次的数字。
输入: [4, 1, 2, 1, 2, 3, 5, 5]
输出: 3 和 4

思路：
1. 准备集合A和列表B，集合A用来存储出现的数字，集合B用来记录只出现过1次的数字
2. 将出现的数字和集合A判断，如果集合A中有数字，说明这个数字出现过，将数字从集合B
中删除。
如果A中没有这个数字，说明数字没出现过，将数字放入集合A和集合B
3. 最后循环结束，打印集合B，就是只出现一次的数字了
"""

num_list = [4, 1, 2, 1, 2, 3, 5, 5]
set_a = set() # 存储所有出现过的数字
set_b = set() # 只出现过一次

for num in num_list:
    if num not in set_a:
        set_a.add(num)
        set_b.add(num)
    else:
        set_b.remove(num)

print('出现次数==1的数字: ')
for num in set_b:
    print(num, end='\t')
print()

