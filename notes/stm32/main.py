import serial

def ping_pong(ser):
    ser.flush()
    ser.write(b"ping")
    ser.flush()
    pong = ser.read(10)
    print(str(pong, 'ascii'))

def run():
    ser.write(b"rand")
    output = ser.read(10000)
    print(str(output, 'ascii'))

def file_cache():
    ser.write(b"file cache 2")
    output = ser.read(10000)
    print(str(output, 'ascii'))

def file_load():
    ser.write(b"file load 4 i*4")
    output = ser.read(10000)
    print(str(output, 'ascii'))
    # w for range(1, 1000)
    # int.from_bytes(zmienna, 'big')

def status():
    return

def file_list():
    ser.write(b"file list")
    list = ser.read(10000)
    print(str(list, 'ascii'))

ser = serial.Serial(port='COM3', baudrate=115200, timeout=0.2)
# ping_pong(ser)
# file_list()
run()
file_cache()
file_load()

# rand
# file cache 2
# file list


