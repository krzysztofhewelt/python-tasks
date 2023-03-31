from tkinter import *
from conn import Database
from matplotlib import pyplot as plt
import pandas as pd


conn = Database()

def get_data_and_draw_charts():
    start = E1.get()
    stop = E2.get()

    elements = []

    elements.append('time')

    if var1.get():
        elements.append('temperature')

    if var2.get():
        elements.append('voltage')

    if var3.get():
        elements.append('humidity')

    elementss = ','.join(elements)
    print(elementss)

    id = variable.get()
    data = conn.fetch(f"SELECT {elementss} FROM data WHERE device_id = {id} AND time BETWEEN '{start}' AND '{stop}'")
    # transpose array to the DataFrame using Pandas
    df = pd.DataFrame(data, columns=elements)
    print("Transposed array to DataFrame:")
    print(df['time'])

    # draw plots
    plt.rcParams["figure.figsize"] = (16, 9)

    if 'temperature' in elements:
        plt.subplot(3, 1, 1)
        plt.plot(df['time'], df['temperature'])
        plt.title('Temperature')
        plt.xlabel('Time')
        plt.ylabel('Temperature [degrees Celsius]')

    if 'humidity' in elements:
        plt.subplot(3, 1, 2)
        plt.plot(df['time'], df['humidity'], '-g')
        plt.title('Humidity')
        plt.xlabel('Time')
        plt.ylabel('Humidity [%]')

    if 'voltage' in elements:
        plt.subplot(3, 1, 3)
        plt.plot(df['time'], df['voltage'], '-r')
        plt.title('Voltage [V]')
        plt.xlabel('Time')
        plt.ylabel('Voltage [V]')


    plt.subplots_adjust(hspace=0.5)  # add some space between plots
    plt.show()


# get devices from database

devices = conn.fetch("SELECT id, name FROM devices")

names = dict()
for name in devices:
    print(name)
    names[name[0]].append()


master = Tk()
master.geometry("500x250")

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()

L1 = Label(master, text="start")
L1.pack()
E1 = Entry(master, bd =5)
E1.pack()

L2 = Label(master, text="stop")
L2.pack()
E2 = Entry(master, bd =5)
E2.pack()

c1 = Checkbutton(master, text='temperature',variable=var1, onvalue=1, offvalue=0)
c1.pack()
c2 = Checkbutton(master, text='voltage',variable=var2, onvalue=1, offvalue=0)
c2.pack()
c3 = Checkbutton(master, text='humidity',variable=var3, onvalue=1, offvalue=0)
c3.pack()

variable = StringVar(master)
variable.set("Select one")

w = OptionMenu(master, variable, *names)
w.pack()

submit_button = Button(master, text='Display', command=get_data_and_draw_charts)
submit_button.pack()

mainloop()