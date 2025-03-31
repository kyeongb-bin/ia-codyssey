import random
import time
import threading

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
            self.sum_values['mars_base_internal_temperature'] += sensor_data['mars_base_internal_temperature']
            self.sum_values['mars_base_external_temperature'] += sensor_data['mars_base_external_temperature']
            self.sum_values['mars_base_internal_humidity'] += sensor_data['mars_base_internal_humidity']
            self.sum_values['mars_base_external_illuminance'] += sensor_data['mars_base_external_illuminance']
            self.sum_values['mars_base_internal_co2'] += sensor_data['mars_base_internal_co2']
            self.sum_values['mars_base_internal_oxygen'] += sensor_data['mars_base_internal_oxygen']
            self.count += 1

            print("Current Environment Data:")
            print(self.env_values)

            if self.count % 60 == 0:  # 5분마다 평균 출력
                avg_values = {
                    'mars_base_internal_temperature': self.sum_values['mars_base_internal_temperature'] / self.count,
                    'mars_base_external_temperature': self.sum_values['mars_base_external_temperature'] / self.count,
                    'mars_base_internal_humidity': self.sum_values['mars_base_internal_humidity'] / self.count,
                    'mars_base_external_illuminance': self.sum_values['mars_base_external_illuminance'] / self.count,
                    'mars_base_internal_co2': self.sum_values['mars_base_internal_co2'] / self.count,
                    'mars_base_internal_oxygen': self.sum_values['mars_base_internal_oxygen'] / self.count
                }
                print("Average Environment Data for the last 5 minutes:")
                print(avg_values)
                self.sum_values = {
                    'mars_base_internal_temperature': 0,
                    'mars_base_external_temperature': 0,
                    'mars_base_internal_humidity': 0,
                    'mars_base_external_illuminance': 0,
                    'mars_base_internal_co2': 0,
                    'mars_base_internal_oxygen': 0
                }
                self.count = 0

            time.sleep(5)

def stop_system(mc):
    input("Press Enter to stop the system...")
    mc.running = False
    print("System stopped....")

if __name__ == "__main__":
    mc = MissionComputer()
    t = threading.Thread(target=stop_system, args=(mc,))
    t.start()
    mc.get_sensor_data()
