import random
import time
import threading
import json
import platform
import os
import subprocess

# 환경 변수 초기화
env_values = {
    'mars_base_internal_temperature': 0,
    'mars_base_external_temperature': 0,
    'mars_base_internal_humidity': 0,
    'mars_base_external_illuminance': 0,
    'mars_base_internal_co2': 0,
    'mars_base_internal_oxygen': 0
}

class DummySensor:
    def __init__(self):
        self.env_values = env_values

    def set_env(self):
        '''환경 데이터를 임의로 설정'''
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        '''환경 데이터를 반환'''
        self.set_env()
        return self.env_values

class MissionComputer:
    def __init__(self):
        # 환경 변수 초기화
        self.env_values = env_values
        # 누적 합계와 카운터 초기화
        self.sum_values = {key: 0 for key in self.env_values}
        self.count = 0
        # 시스템 실행 상태 플래그
        self.running = True

    def get_mission_computer_info(self):
        '''미션 컴퓨터의 시스템 정보를 JSON 형식으로 반환'''
        try:
            system_info = {
                'Operating System': platform.system(),
                'OS Version': platform.version(),
                'CPU Type': platform.processor(),
                'CPU Cores': os.cpu_count(),
                'Memory Size (GB)': round(
                    os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024 ** 3), 2
                )
            }

            # setting.txt 파일에서 출력 항목 설정 읽기
            if os.path.exists('setting.txt'):
                with open('setting.txt', 'r') as file:
                    settings = file.read().splitlines()
                    system_info = {key: system_info[key] for key in settings if key in system_info}

            return json.dumps(system_info, indent=4)
        except Exception as e:
            return json.dumps({'error': str(e)}, indent=4)

    def get_mission_computer_load(self):
        '''미션 컴퓨터의 부하 정보(CPU 및 메모리 사용량)를 JSON 형식으로 반환'''
        try:
            if platform.system() == 'Darwin':  # macOS
                # CPU 사용량 계산 (ps 명령어 사용)
                cpu_usage = subprocess.check_output(
                    "ps -A -o %cpu | awk '{s+=$1} END {print s}'",
                    shell=True
                ).decode().strip()

                # 메모리 사용량 계산 (vm_stat 명령어 사용)
                vm_stat_output = subprocess.check_output("vm_stat", shell=True).decode()
                vm_stat_lines = vm_stat_output.splitlines()

                # 페이지 크기 추출 (첫 번째 줄에서 숫자만 가져오기)
                page_size_kb = int(vm_stat_lines[0].split()[-2]) // 1024

                # 메모리 통계 추출
                memory_stats = {}
                for line in vm_stat_lines[1:]:
                    if ':' in line:
                        key, value = line.split(':')
                        key = key.strip()
                        value = value.strip().split()[0]  # 숫자 부분만 추출
                        memory_stats[key] = int(float(value))  # 소수점 처리 후 정수 변환

                # 총 페이지 수 및 사용된 페이지 수 계산
                total_pages = sum(memory_stats[key] for key in ['Pages free', 'Pages active', 'Pages inactive', 'Pages speculative'])
                used_pages = total_pages - memory_stats['Pages free']
                mem_usage = round((used_pages / total_pages) * 100, 2)

            elif platform.system() == 'Linux':
                # CPU 사용량 계산 (top 명령어 사용)
                cpu_usage = subprocess.check_output(
                    "top -bn1 | grep '%Cpu(s)' | awk '{print $2}'",
                    shell=True
                ).decode().strip()

                # 메모리 사용량 계산 (free 명령어 사용)
                mem_info = subprocess.check_output(
                    "free -m | awk '/Mem:/ {print $3/$2 * 100.0}'",
                    shell=True
                ).decode().strip()
                mem_usage = float(mem_info)

            else:  # Windows 환경 대체 코드
                cpu_usage = subprocess.check_output(
                    "wmic cpu get loadpercentage",
                    shell=True
                ).decode().strip().split('\n')[1]

                mem_info = subprocess.check_output(
                    "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value",
                    shell=True
                ).decode().strip()

                mem_info_lines = mem_info.splitlines()
                free_memory = int(mem_info_lines[0].split('=')[1])
                total_memory = int(mem_info_lines[1].split('=')[1])

                mem_usage = round((1 - free_memory / total_memory) * 100, 2)

            load_info = {
                'CPU Usage (%)': float(cpu_usage),
                'Memory Usage (%)': mem_usage
            }

            return json.dumps(load_info, indent=4)
        except Exception as e:
            return json.dumps({'error': str(e)}, indent=4)

    def get_sensor_data(self):
        '''센서 데이터를 수집하고 출력'''
        ds = DummySensor()
        while self.running:
            sensor_data = ds.get_env()
            self.env_values = sensor_data

            # 누적 합계 계산
            for key in self.env_values:
                self.sum_values[key] += sensor_data[key]
            self.count += 1

            print('현재 환경 데이터 (JSON):')
            print(json.dumps(self.env_values, indent=4))

            if self.count % 60 == 0:  # 매 5분마다 평균 출력 (5초 간격 * 60회 반복)
                avg_values = {key: self.sum_values[key] / self.count for key in self.env_values}
                print('지난 5분간 평균 환경 데이터 (JSON):')
                print(json.dumps(avg_values, indent=4))
                
                # 누적 합계 및 카운터 초기화
                self.sum_values = {key: 0 for key in self.env_values}
                self.count = 0

            time.sleep(5)

    def stop_system(self):
        '''사용자가 입력하면 시스템 종료'''
        input('Enter 키를 눌러 시스템을 종료하세요...')
        self.running = False
        print('시스템이 종료되었습니다.')

if __name__ == '__main__':
    # MissionComputer 클래스를 runComputer라는 이름으로 인스턴스화합니다.
    runComputer = MissionComputer()

    print('=== 미션 컴퓨터 시스템 보고서 ===')
    print(runComputer.get_mission_computer_info())

    print('=== 미션 컴퓨터 부하 정보 ===')
    print(runComputer.get_mission_computer_load())

    stop_thread = threading.Thread(target=runComputer.stop_system)
    stop_thread.start()
    
    runComputer.get_sensor_data()
