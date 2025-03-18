# Mars_Base_Inventory_List.csv 파일을 읽어 리스트로 변환
try:
    with open('./Mars_Base_Inventory_List.csv', 'r') as file:
        lines = file.readlines()
    header = lines[0].strip().split(',')
    inventory = [line.strip().split(',') for line in lines[1:]]
except FileNotFoundError:
    print('Error: 파일을 찾을 수 없습니다.')
except Exception as e:
    print(f'Error: {e}')

# 인화성 지수로 정렬
inventory.sort(key=lambda x: float(x[4]), reverse=True)

# 인화성 지수가 0.7 이상인 항목을 별도로 출력
high_flammability = [item for item in inventory if float(item[4]) >= 0.7]
print('인화성 지수 >= 0.7:')
for item in high_flammability:
    print(','.join(item))

# 인화성 지수가 0.7 이상인 항목을 CSV 파일로 저장
try:
    with open('./Mars_Base_Inventory_danger.csv', 'w') as file:
        file.write(','.join(header) + '\n')
        for item in high_flammability:
            file.write(','.join(item) + '\n')
except Exception as e:
    print(f'Error: {e}')

# 전체 인벤토리를 인화성 지수로 정렬하여 Mars_Base_Inventory_List.csv 파일로 저장
try:
    with open('./Mars_Base_Inventory_List.csv', 'w') as file:
        file.write(','.join(header) + '\n')
        for item in inventory:
            file.write(','.join(item) + '\n')
except Exception as e:
    print(f'Error: {e}')
