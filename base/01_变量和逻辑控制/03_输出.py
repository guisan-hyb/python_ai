name = 'guisan'
age = 19
weight = 72

score = 98.231312

print(name)
print(age)
print(weight)
print(score)

print(f"姓名: {name}, 年龄: {age}, 体重: {weight}")
print(f'分数: {score:.2f}')
print(f'学号: {1:06}')

# format
print("姓名: {}, 年龄: {}, 体重: {}".format(name, age, weight))
print("姓名: {1}, 年龄: {0}".format(age, name))

print("姓名: %s, 年龄: %d, 成绩: %.2f" % (name,age,score))

print("hello I'm guisan")
print('hello I\'m guisan')

