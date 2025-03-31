import random
import time
import threading
import json

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        self.set_env()
        return self.env_values

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.sum_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.count = 0
        self.running = True

    def get_sensor_data(self):
        ds = DummySensor()
        while self.running:
            sensor_data = ds.get_env()
            self.env_values = sensor_data
            for key in self.env_values:
                self.sum_values[key] += sensor_data[key]
            self.count += 1

            print('Current Environment Data (JSON):')
            print(json.dumps(self.env_values, indent=4))

            if self.count % 60 == 0:  # 5분마다 평균 출력 (5초 간격 * 60 = 5분)
                avg_values = {key: self.sum_values[key] / self.count for key in self.env_values}
                print('Average Environment Data for the last 5 minutes (JSON):')
                print(json.dumps(avg_values, indent=4))
                self.sum_values = {key: 0 for key in self.env_values}
                self.count = 0

            time.sleep(5)

    def stop_system(self):
        input('Press Enter to stop the system...')
        self.running = False
        print('System stopped....')

if __name__ == '__main__':
    RunComputer = MissionComputer()
    stop_thread = threading.Thread(target=RunComputer.stop_system)
    stop_thread.start()
    RunComputer.get_sensor_data()
