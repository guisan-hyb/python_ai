total_people = int(input('输入参与活动的人数: '))
total_col = float(input('输入活动总花费: '))

if total_people < 1:
    print('至少1人')
else:
    manage_fee = total_col*0.1
    final_col = total_col+manage_fee
    per_people_col = final_col/total_people

    print('='*30)
    print(f'原始活动花费: {total_col:.2f}元')
    print(f'10%活动管理费: {manage_fee:.2f}元')
    print(f'最终总费用: {final_col:.2f}元')
    print(f'每人均摊: {per_people_col:.2f}元')
    print('='*30)


