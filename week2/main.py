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
print('-----인화성 지수 >= 0.7-----')
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

# 보너스 과제: 인화성 순서로 정렬된 배열의 내용을 이진 파일형태로 저장
try:
    with open('Mars_Base_Inventory_List.bin', 'wb') as binary_file:
        for item in inventory:
            # Join the item list into a single string and encode it to bytes
            binary_file.write((','.join(item) + '\n').encode('utf-8'))
except Exception as e:
    print(f'Error while saving to binary file: {e}')

# 보너스 과제: 저장된 Mars_Base_Inventory_List.bin의 내용을 다시 읽어 들여서 화면에 내용을 출력
try:
    with open('Mars_Base_Inventory_List.bin', 'rb') as binary_file:
        content = binary_file.read().decode('utf-8')
        print('-----Mars_Base_Inventory_List.bin 내용-----')
        print(content)
except Exception as e:
    print(f'Error while reading from binary file: {e}')
