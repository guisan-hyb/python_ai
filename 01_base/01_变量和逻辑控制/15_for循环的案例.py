'''
案例：用for循环实现用户登录

① 输入用户名和密码

② 判断用户名和密码是否正确（username='student'，password='python123'）

③ 登录仅有2次机会，超过2次会提示“登录失败，次数已用完”

分析：用户登陆情况有3种:

① 用户名错误(此时便无需判断密码是否正确) -- 登陆失败

② 用户名正确 密码错误 --登陆失败

③ 用户名正确 密码正确 --登陆成功
'''


b_success = False

for i in range(2):
    name = input('输入用户名: ')
    pwd = input('输入密码: ')
    if name == 'student' and pwd == 'python123':
        print('登陆成功')
        b_success = True
        break
    print('输入错误, 重试')

if b_success:
    print('登陆成功后的其他操作')
else:
    print('两次机会用尽')

