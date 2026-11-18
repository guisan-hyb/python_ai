# 单层上，好比传了个对象指针，可以更改对象的内容，但是不能更改对象本身

def f(x):
    print(id(x))

a = []
print(id(a))
f(a)


def f1(x):
    x.append(1)

a = []
f1(a)
print(a)


def f2(x):
    x = [1,2,3]

a = []
f2(a)
print(a)


# 但遇到嵌套结构时要记住：指针副本只保证“第一层绑定”是局部的，里面指向的对象仍然是共享的：
def f3(p):
    p[0] = 99

a = [[1]]
f3(a)
print(a)

