tuple1 = ('炸鸡',True,25.5)
# 拆包
name, is_flag, price = tuple1
print(f'{name},{is_flag},{price}')

a,b = (10,20)
print(f'{a},{b}')

c1 = 'a'
c2 = 'b'
tmp = c1
c1 = c2
c2 = tmp
print(f'{c1},{c2}')

c2,c1 = (c1,c2)
print(f'{c1},{c2}')

