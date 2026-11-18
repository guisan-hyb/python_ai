'''
### 案例需求（全新）

判断相邻元素的变化趋势

给定一个正整数数组，判断每一对相邻元素是“上升”“下降”还是“相等”，并输出结果列表

例如：
 输入: `[3, 5, 5, 2, 4]`
 输出: `['上升', '相等', '下降', '上升']`
'''


last = None
num_list = [3,5,5,2,4]
res_list = []
for cur in num_list:
    if last == None:
        res_list.append('up')
    elif cur > last:
        res_list.append('up')
    elif cur < last:
        res_list.append('down')
    else:
        res_list.append('eql')
    last = cur

print('res_list: ',res_list)


'''
找出列表中第一次出现的重复元素

给定一个列表，找到**第一个重复出现的元素**（只要出现第二次就算重复），并输出该元素

例如：
 输入: `[2, 3, 5, 3, 6, 5, 7]`
 输出: `3`
'''

src_list = [2,3,5,3,6,5,7]
back_list = []
duplicate_num = None

for cur in src_list:
    if cur in back_list:
        duplicate_num = cur
        break
    back_list.append(cur)
if duplicate_num:
    print(f'重复元素为: ',duplicate_num)
else:
    print('不存在重复元素')

