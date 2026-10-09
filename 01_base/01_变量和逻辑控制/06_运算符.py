a = 10
b = 3

print(f'{a}+{b}={a+b}')
print(f'{a}*{b}={a*b}')
print(f'{a}-{b}={a-b}')
print(f'{a}/{b}={a/b}')
print(f'{a}//{b}={a//b}')
print(f'{a}%{b}={a%b}')
print(f'{a}**{b}={a**b}')

a**=b
print(a)

print(f'a >= b = {a >= b}')
print(f'a <= b = {a <= b}')
print(f'a > b = {a > b}')
print(f'a < b = {a < b}')
print(f'a == b = {a == b}')
print(f'a != b = {a != b}')

print(a>b and a<b)
print(a>b or a<b)
print(not a>b)
