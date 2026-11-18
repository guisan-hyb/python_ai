'''
演示列表的查找操作
'''
from itertools import count

'''
列表名[下标]  获取指定下标的元素
count()   统计指定数据在当前列表中出现的次数
index() 获取指定数据所在位置的下标
in 判断某个元素是否在列表中, 如果在则返回True
not in 判断某个元素是否不在列表中, 如果不在则返回True
'''
# 定义列表
name_list = ['小明','小红','小刚','小丽','小强','zack','Ray','Lucy','Lily','小丽']
index = name_list.index('zack')
print(index)

count = name_list.count('小丽')
print(count)

if '小刚' in name_list:
    print('1')
else:
    print('0')

if 'saf' in name_list:
    print(1)
else:
    print(0)


'''
append() 在列表后面添加元素
extend() 在列表的结尾追加数据，extend出传递的是一个序列，将这个序列的
每一个元素逐一添加到列表中
insert() 插入，在指定位置新增数据
两个列表相加 list1+list2，相当于将list2中的内容依次取出放入list1中
'''
name_list2 = ['a','b']
name_list.extend(name_list2)
print(name_list)
name_list.append('s')
print(name_list)
name_list.insert(2,'ds')
print(name_list)

list1 = [1,2,3,4,5]
list2 = [6,7,8,9]
list3 = list1+list2
print(list3)


'''
元素删除
del 列表[下标] 删除指定下标的元素
列表.pop() 删除最后一个元素
列表.pop(索引) 根据索引删除元素
'''
del list3[-1]
print(list3)
del_num = list3.pop()
print(f'del_num: {del_num}')
print(f'list3: {list3}')
del_num = list3.pop(2)
print(f'del_num: {del_num}')
print(f'list3: {list3}')
