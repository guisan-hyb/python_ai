'''
演示列表推导式
'''

'''
变量名 = [表达式 for 变量 in 序列]
变量名 = [表达式 for 变量 in 序列 if 判断条件]
变量名 = [表达式 for 变量 in 序列 for 变量2 in 序列2]
'''

new_list = [i for i in range(10)]
print(new_list)

print([i for i in range(10) if i % 2 ==0])


seats = []
for row in range(3):
    for col in range(4):
        seat = (row,col)
        seats.append(seat)
        #seats.append((row,col))
print(seats)


seats = [(row,col) for row in range(3) for col in range(4)]
print(seats)


'''
案例一：使用列表推导式生成平方数集合

例如, 用户输入10, 表示要生成 1~10的每一个数字的平方的集合
'''

'''
变量名称 = {表达式 for 变量 in 序列}
'''
square_set = {ele ** 2 for ele in range(1, 11)}
print(square_set)
