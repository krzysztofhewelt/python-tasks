# transponowanie (wiersze na kolumny)
# wyswietlenie matplotlib (trzy wykresy) subplots
# na argumenty lub plik konfig (measurement time i insert time)
# DBNAME + connection strings -> config file (config.ini)
# device ID wstawić w config

import time
import random
from conn import Database
from datetime import datetime


# voltage - 3 - 5 [V]
conn = Database(db='iot', host='localhost', user='root', password='admin123')

DEVICE_ID = 1
voltage = random.uniform(3.0, 5.0)
temperature = random.uniform(19.0, 25.0)
humidity = random.uniform(50, 70)

MEASUREMENT_TIME = 1
INSERT_TIME = 5
n = int(INSERT_TIME / MEASUREMENT_TIME)
i = 0

sql = ""

while True:
    dt = datetime.now()
    now = dt.strftime('%Y-%m-%d %H:%M:%S')

    voltage += random.uniform(-0.01, 0)
    temperature += random.uniform(-0.5, 0.5)
    humidity += random.uniform(-1.0, 1.0)

    sql += f"INSERT INTO data VALUES (NULL, {DEVICE_ID}, '{now}', {temperature}, {humidity}, {voltage}); "

    i += 1
    if i >= n:
        i = 0
        conn.execute(str(sql))
        print("Added to database")

    print(f"Time: {now}, Voltage: {voltage}, Temperature: {temperature}, Humidity: {humidity}")

    time.sleep(MEASUREMENT_TIME)

