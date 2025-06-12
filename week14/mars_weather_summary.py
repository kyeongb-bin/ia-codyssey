import csv
import mysql.connector

class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.connection = None
        self.cursor = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def executemany(self, query, params_list):
        self.cursor.executemany(query, params_list)

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

def create_mars_weather_table(helper):
    create_table_query = (
        'CREATE TABLE IF NOT EXISTS mars_weather ('
        'weather_id INT AUTO_INCREMENT PRIMARY KEY, '
        'mars_date DATETIME NOT NULL, '
        'temp INT, '
        'storm INT'
        ')'
    )
    helper.execute(create_table_query)
    helper.commit()

def read_csv_data(csv_path):
    data = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mars_date = row['mars_date']
            temp = int(row['temp'])
            storm = int(row['storm'])
            data.append((mars_date, temp, storm))
    return data

def insert_mars_weather_data(helper, data):
    insert_query = (
        'INSERT INTO mars_weather (mars_date, temp, storm) '
        'VALUES (%s, %s, %s)'
    )
    helper.executemany(insert_query, data)
    helper.commit()

def summarize_data(data):
    count = len(data)
    temp_sum = sum(row[1] for row in data)
    storm_count = sum(row[2] for row in data)
    if count > 0:
        avg_temp = temp_sum / count
    else:
        avg_temp = 0
    summary = (
        f'총 데이터 수: {count}\n'
        f'평균 온도: {avg_temp:.2f}\n'
        f'폭풍 발생 횟수: {storm_count}\n'
    )
    with open('mars_weather_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    print(summary)

def main():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'your_password',
        'database': 'your_database'
    }
    csv_path = 'mars_weathers_data.csv'

    helper = MySQLHelper(
        db_config['host'],
        db_config['user'],
        db_config['password'],
        db_config['database']
    )
    helper.connect()
    create_mars_weather_table(helper)

    data = read_csv_data(csv_path)
    insert_mars_weather_data(helper, data)
    summarize_data(data)

    helper.close()

if __name__ == '__main__':
    main()
