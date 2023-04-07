from datetime import datetime
from functools import partial
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from matplotlib import pyplot as plt

import pandas as pd

from conn import Database


class Validator:

    def validate_types_of_measurements(self, temperature, humidity, voltage):
        if not temperature and not humidity and not voltage:
            return False
            self.errors += "- You must choose at least one type of measurement\n"

        return True

    def check_device_id(self, device_name):
        if Devices.get_device_id(device_name) is None:
            return False
            self.errors += "- Device not found\n"

        return True

    def check_start_date(self, start):
        if start:
            try:
                datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
                return True
            except ValueError:
                return False
                self.errors += "- Start time is not valid date!\n"

        return None

    def check_stop_date(self, stop):
        if stop:
            try:
                datetime.strptime(stop, "%Y-%m-%d %H:%M:%S")
                return True
            except ValueError:
                return False
                self.errors += "- Stop time is not valid date!\n"

        return None

    def validate_dates(self, start, stop):
        validated_start = self.check_start_date(start)
        validated_stop = self.check_stop_date(stop)

        if validated_start is False or validated_stop is False:
            return False

        if self.check_start_date(start) and self.check_stop_date(stop):
            start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            stop_date = datetime.strptime(stop, "%Y-%m-%d %H:%M:%S")

            if start_date and stop_date and start_date > stop_date:
                return False
                self.errors += "- Start time must be less or equal to stop time\n"

        return True

    def validate_all(self, device_name, temperature, humidity, voltage, start, stop):
        return self.validate_types_of_measurements(temperature, humidity, voltage) and self.check_device_id(
            device_name) and self.validate_dates(start, stop)


class Devices:
    devices = dict()

    def __init__(self):
        self.conn = Database()
        self.get_devices_from_database()

    def get_devices_from_database(self):
        devices = self.conn.fetch("SELECT id, name FROM devices")
        for device in devices:
            self.devices[device[1]] = device[0]

    def get_device_names_list(self):
        return list(self.devices.keys())

    @staticmethod
    def get_device_id(name):
        try:
            return Devices.devices[name]
        except KeyError:
            return None

    def make_data_columns_list(self, temperature, humidity, voltage):
        columns = ['time']

        if temperature:
            columns.append('temperature')

        if voltage:
            columns.append('voltage')

        if humidity:
            columns.append('humidity')

        return columns

    def device_probes_from_database(self, device_name, temperature, humidity, voltage, start, stop):
        print(device_name)
        dev_id = self.get_device_id(str(device_name))
        start_time = start
        stop_time = stop
        columns = self.make_data_columns_list(temperature, humidity, voltage)
        columns_joined = ','.join(columns)

        query = f"SELECT {columns_joined} FROM data WHERE device_id = {dev_id} "

        if start_time:
            query += f"AND time >= '{start_time}'"

        if stop_time:
            query += f"AND time <= '{stop_time}'"

        data = self.conn.fetch(query)
        df = pd.DataFrame(data, columns=columns)
        if df.empty:
            messagebox.showinfo("No data", "There is nothing to show")
            return

        return df


class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x250")
        self.master.title("IoT Visualizer")

        self.devices = Devices()

        self.make_controls()

    def make_controls(self):
        temperature = IntVar()
        voltage = IntVar()
        humidity = IntVar()
        device = StringVar()

        temperature_checkbox = Checkbutton(self.master, text='temperature', variable=temperature, onvalue=1, offvalue=0)
        temperature_checkbox.pack()
        voltage_checkbox = Checkbutton(self.master, text='voltage', variable=voltage, onvalue=1, offvalue=0)
        voltage_checkbox.pack()
        humidity_checkbox = Checkbutton(self.master, text='humidity', variable=humidity, onvalue=1, offvalue=0)
        humidity_checkbox.pack()

        label_start = Label(self.master, text="start date:")
        label_start.pack()
        entry_start = Entry(self.master)
        entry_start.pack()

        label_stop = Label(self.master, text="stop date:")
        label_stop.pack()
        entry_stop = Entry(self.master)
        entry_stop.pack()

        label_devices = Label(self.master, text="available devices:")
        label_devices.pack()
        devices_list = Combobox(self.master, textvariable=device, state="readonly",
                                values=self.devices.get_device_names_list())
        devices_list.pack()

        submit_button = Button(self.master, text='Display chart',
                               command=partial(self.test, device, temperature, humidity, voltage,
                                               entry_start, entry_stop),
                               width=20, height=5)
        submit_button.pack()

    def test(self, device, temperature, humidity, voltage, entry_start, entry_stop):
        validate = Validator()
        if not validate.validate_all(device.get(), temperature.get(), humidity.get(), voltage.get(), entry_start.get(),
                                     entry_stop.get()):
            messagebox.showerror('Error', 'some errors')
            return

        df = self.devices.device_probes_from_database(device.get(), temperature.get(), humidity.get(), voltage.get(),
                                                      entry_start.get(), entry_stop.get())
        self.draw_chart(df)

    def draw_chart(self, df):
        if not df:
            return

        plt.rcParams["figure.figsize"] = (16, 9)

        fig, axs = plt.subplots(nrows=len(df.columns) - 1, squeeze=False, sharex=True)
        i = 0

        if 'temperature' in df:
            axs[i, 0].plot(df['time'], df['temperature'], label="Temperature")
            axs[i, 0].grid(visible=True, axis='x')
            axs[i, 0].legend()
            axs[i, 0].set_xlabel('Time')
            axs[i, 0].set_ylabel('Temperature [degrees Celsius]')
            i += 1

        if 'humidity' in df:
            axs[i, 0].plot(df['time'], df['humidity'], '-g', label='Humidity')
            axs[i, 0].grid(visible=True, axis='x')
            axs[i, 0].legend()
            axs[i, 0].set_xlabel('Time')
            axs[i, 0].set_ylabel('Humidity [%]')
            i += 1

        if 'voltage' in df:
            axs[i, 0].plot(df['time'], df['voltage'], '-r', label='Voltage')
            axs[i, 0].grid(visible=True, axis='x')
            axs[i, 0].legend()
            axs[i, 0].set_xlabel('Time')
            axs[i, 0].set_ylabel('Voltage [V]')
            i += 1

        axs[0, 0].set_title('Data visualization')
        plt.subplots_adjust(hspace=.0)  # add some space between plots
        plt.show()


root = Tk()
app = MainApplication(root)
root.mainloop()
