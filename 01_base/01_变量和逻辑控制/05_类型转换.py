age = 100
print(type(age))
agr = 3.21
print(type(age))
age = 'asfcfas'
print(type(age))


product_name = input("商品名称: ")
price_str = input("商品单价: ")
count_str = input("商品数量: ")

price = float(price_str)
count = int(count_str)

sum = price * count
print(f'购买{product_name}的数目为: {count}\n'
      f'总价为: {sum:.3f}')


print('*'*20)
print('1'*20)
