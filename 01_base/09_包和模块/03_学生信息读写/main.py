from info_utils import utils

if __name__ == '__main__':
    students = utils.read_students_csv('./students.csv')
    print(students)
    print(utils.calculate_average(students))
    utils.save_report('./students.json', students)

# from info_utils import *
# if __name__ == '__main__':
#     students = read_students_csv('./students.csv')
#     print(students)
#     print(calculate_average(students))
#     save_report('./students.json', students)

