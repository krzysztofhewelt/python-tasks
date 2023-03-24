from conn import Database

# creating database
DBNAME = 'iot'
conn = Database(db=None, host='localhost', user='root', password='admin123')
conn.execute(f'DROP DATABASE IF EXISTS {DBNAME}')
conn.execute(f'CREATE DATABASE {DBNAME}')
conn.db = DBNAME

conn.execute("""
CREATE TABLE IF NOT EXISTS `devices` (
    id INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    uid CHAR(24) NOT NULL,
    name VARCHAR(255),
    measurement_interval INT UNSIGNED NOT NULL DEFAULT 5,
    transceive_interval INT UNSIGNED NOT NULL DEFAULT 60,
    PRIMARY KEY(id)
);
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS `data` (
    id INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
    device_id INT UNSIGNED NOT NULL,
    time DATETIME NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    voltage FLOAT,
    PRIMARY KEY (id),
    FOREIGN KEY (device_id) REFERENCES devices(id),
    INDEX device_time (device_id, time)
);
""")

conn.execute("""
INSERT INTO devices
VALUES (
    NULL,
    "000000000000000000000000",
    "Test device",
    1,
    5
);
""")