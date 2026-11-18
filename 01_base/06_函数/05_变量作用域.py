'''
演示全局变量和局部变量
'''

'''
全局变量： 定义在函数外部的变量就是全局变量
局部变量： 定义在函数内部的变量，就是局部变量
全局变量的作用范围：是整个全局的作用范围，一旦定义全局变量，在当前的文件的任意位置
都可以被使用
局部变量的作用范围：仅在当前这个函数的内部，一旦出了函数，该变量就被销毁了
'''

a = 100
def func1():
    b = 200
    print(f'函数内输出a: {a}')
    print(f'函数内输出b: {b}')

func1()


print(f'函数外输出a: {a}')

# 没有对变量名赋值就不用写 global

'''
在Python中有两种类型的变量
1. 可变类型 list,dict,set,自定义的类型 ，尽管数据相同，但是占用不同的内存空间
2. 不可变类型 int, bool, str, double, tuple,相同的数据在内存中只存储1份数据
a = 1
b = 1
可以理解为a和b存储的都是1的地址
当a = 2 的时候，a指向的就是2的地址
'''

a = 1
b = 1
c = 2

list_a = [1,2,3]
list_b = [1,2,3]
list_a.append(4)
print(list_a)
print(list_b)


'''
因为Python中赋值和定义具有二义性
Python不同于C++， 
C++语法
int a = 100;  a = 200;
Python中
定义和赋值弄到一起
a = 100
a = 200
如果a = 200在函数内， a = 100在函数外
两个a 不是同一个a， 函数内的a = 200会被认为定义了一个新的变量a
'''

# lt = [2*i for i in range(0,10)]
# print(lt)

num = 10
def func():
    num = 20
    print(f'函数内num: {num}, id(num): {id(num)}')

func()

print(f'函数外num: {num}, id(num): {id(num)}')

print('*'*50)


def func2():
    # 想要通过函数内部修改外部的全局变量，需要使用global
    # num被声明为全局变量
    global num
    num = 30
    print(f'函数内num: {num}, id(num): {id(num)}')

func2()
print(f'函数外num: {num}, id(num): {id(num)}')


person = {'name': 'zack','age':25}
print(f'函数外全局变量person: {person}, id(person): {id(person)}')

def func_dict():
    # 没有对变量名赋值就不用写 global
    person['address'] = 'nanjing'
    print(f'函数内打印全局变量person: {person}, id(person): {id(person)}')

func_dict()

# 在全局范围内打印全局变量
print(f'调用完func1,在函数外打印person: {person}, id(person): {id(person)}')

