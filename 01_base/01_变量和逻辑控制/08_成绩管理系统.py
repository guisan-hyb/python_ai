student_name = input('输入姓名: ')
chinese_str = input('输入语文成绩: ')
math_str = input('输入数学成绩: ')
english_str = input('输入英语成绩: ')

chinese = float(chinese_str)
math = float(math_str)
english = float(english_str)

total_score = chinese+math+english
aver_score = total_score/3

if aver_score>=90:
    grade = 'a'
elif aver_score>=80:
    grade = 'b'
elif aver_score>=70:
    grade = 'c'
else:
    grade = 'd'

print('='*40)
print(f'学生姓名: {student_name}')
print(f'语文成绩: {chinese:.1f}分')
print(f'数学成绩: {math:.1f}分')
print(f'英语成绩: {english:.1f}分')
print(f'总成绩: {total_score:.1f}分')
print(f'平均成绩: {aver_score:.1f}分')
print(f'成绩评级: {grade}')
print('='*40)

