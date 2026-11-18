'''
演示文件读写
'''

'''
1. file = open(文件路径, 模式, 编码)
file是文件对象，里面包含了文件描述符
模式 r 只读，如果文件不存在则报错
w 只写，如果文件不存在则创建，存在则清空并且覆盖写
a 追加，如果文件不存在则创建，存在则追加

2. file.read() 读取  file.write(内容)
3. file.close()
'''

'''
相对路径: 以.或者..开始的路径表示相对路径
.表示当前目录, ..表示上一级目录
./a.txt 表示当前目录下的a.txt文件
../b.txt 表示上一级目录的b.txt文件
绝对路径： linux环境下以/(根目录开始)的路径，就是绝对路径
/home/zack/a.txt 这个就是以/目录开始,home文件夹下zack文件夹下的a.txt
windows的绝对路径是以盘符开始的路径
"D:\\workspace\\github\\python_ai\\base\\06_文件\\01_文件读写.py"
'''

# 创建文件对象
file_w = open('./example.txt','w', encoding='utf-8')
# read()默认读取所有内容，也可以指定读取的大小read(1024)
# write返回实际写入文件的字符数

data = file_w.write('不过是些许风霜罢了')
print(data)

file_w.close()


# 创建文件对象
file_r = open('./example.txt','r',encoding='utf-8')
# read()默认读取所有内容，也可以指定读取的大小read(1024)
data = file_r.read()
print(data)

file_r.close()

# 创建文件对象
file_w = open('./example.txt','a',encoding='utf-8')
# read()默认读取所有内容，也可以指定读取的大小read(1024)
# write返回实际写入文件的字符数
data = file_w.write('\n些许风霜些许愁，无足之鸟不回头')
print(data)

file_w.close()

