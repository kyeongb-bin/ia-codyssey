import random
import datetime

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
        env = self.env_values
        log_entry = f"{datetime.datetime.now()} - 내부 온도: {env['mars_base_internal_temperature']}, 외부 온도: {env['mars_base_external_temperature']}, 내부 습도: {env['mars_base_internal_humidity']}, 외부 광량: {env['mars_base_external_illuminance']}, 내부 CO2: {env['mars_base_internal_co2']}, 내부 산소: {env['mars_base_internal_oxygen']}\n"
        with open('./mars_base_log.txt', 'a') as log_file:
            log_file.write(log_entry)
        return env

# 인스턴스화 및 메소드 호출
ds = DummySensor()
ds.set_env()
print(ds.get_env())
