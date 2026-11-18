'''
演示函数用法
'''

'''
函数先定义再调用
定义:
def func(形参1,形参2,形参3,...):
    函数体
    return 返回值

func如果没有返回值，默认返回None, 相当于return None
函数定义的时候这个参数，叫做形式参数，简称形参

调用:
res = func(实参1, 实参2, 实参3)
res接受func返回值
函数调用时传递给函数的参数叫做实际参数，简称实参
'''

def pick_item():
    print('get one item')

pick_item()
pick_item()
pick_item()

def pick_item2(item_name):
    print(f'pick {item_name}')

pick_item2(24)
pick_item2('67')
pick_item2('man')

bag_capacity = 100
current_count = 0

def pick_item3(item_name):
    global current_count
    if current_count >= bag_capacity:
        return False
    current_count = current_count+1
    print(f'pick {item_name}, {current_count}/{bag_capacity}')
    return True

result = pick_item3('魔剑-阿波菲斯')
if result:
    print('捡道具成功')
else:
    print('背包已满，无法获取')

pick_item3('无影剑雷诺')
if result:
    print('捡道具成功')
else:
    print('背包已满，无法获取')

pick_item3('边境荒火')
if result:
    print('捡道具成功')
else:
    print('背包已满，无法获取')



def return_value():
    return 1
    return 2 # no

print(return_value())


def return_value():
    return 1,2

value = return_value()
print(value)
print(type(value))


def get_value(num1,num2):
    acc = num1*num2
    div = 0
    if num2 != 0:
        div = num1/num2
    add = num1+num2
    sub = num1-num2
    return acc,div,add,sub

# 元组拆包
acc,div,add,sub = get_value(10,5)
print(acc,div,add,sub)

