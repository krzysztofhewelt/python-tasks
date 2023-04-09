from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from conn import Database
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from functools import partial


class Validator:
    @staticmethod
    def validate_types_of_measurements(temperature, humidity, voltage):
        if not temperature and not humidity and not voltage:
            raise ValueError("You must choose at least one type of measurement.")

        return True

    @staticmethod
    def check_device_id(device_name):
        if Devices.get_device_id(device_name) is None:
            raise ValueError("Device not found.")

        return True

    @staticmethod
    def check_start_date(start):
        if start:
            try:
                return datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("Start time is not valid date.")

        return None

    @staticmethod
    def check_stop_date(stop):
        if stop:
            try:
                return datetime.strptime(stop, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("Stop time is not valid date.")

        return None

    def validate_dates(self, start, stop):
        validated_start = self.check_start_date(start)
        validated_stop = self.check_stop_date(stop)

        if validated_start and validated_stop and validated_start > validated_stop:
            raise ValueError("Start time must be less or equal to stop time.")

        return True

    def validate_all(self, device_name, temperature, humidity, voltage, start, stop):
        errors = ""

        try:
            self.validate_types_of_measurements(temperature, humidity, voltage)
        except ValueError as e:
            errors += str(e) + "\n"

        try:
            self.check_device_id(device_name)
        except ValueError as e:
            errors += str(e) + "\n"

        try:
            self.validate_dates(start, stop)
        except ValueError as e:
            errors += str(e) + "\n"

        return errors


class Devices:
    devices = dict()

    def __init__(self):
        self.conn = Database()
        self.get_devices_from_database()

    @staticmethod
    def get_device_names_list():
        return list(Devices.devices.keys())

    @staticmethod
    def get_device_id(name):
        try:
            return Devices.devices[name]
        except KeyError:
            return None

    @staticmethod
    def make_data_columns_list(temperature, humidity, voltage):
        columns = ['time']

        if temperature:
            columns.append('temperature')

        if voltage:
            columns.append('voltage')

        if humidity:
            columns.append('humidity')

        return columns

    def get_devices_from_database(self):
        devices = self.conn.fetch("SELECT id, name FROM devices")
        for device in devices:
            Devices.devices[device[1]] = device[0]

    def device_probes_from_database(self, device_name, temperature, humidity, voltage, start, stop):
        dev_id = self.get_device_id(str(device_name))
        columns = self.make_data_columns_list(temperature, humidity, voltage)
        columns_joined = ','.join(columns)

        query = f"SELECT {columns_joined} FROM data WHERE device_id = {dev_id} "

        if start:
            query += f"AND time >= '{start}'"

        if stop:
            query += f"AND time <= '{stop}'"

        data = self.conn.fetch(query)
        df = pd.DataFrame(data, columns=columns)
        if df.empty:
            messagebox.showinfo("No data", "There is nothing to show")

        return df


class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x250")
        self.master.title("IoT Visualizer")
        self.master.resizable(False, False)

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
                               command=partial(self.validate_and_get_data, device, temperature, humidity, voltage,
                                               entry_start, entry_stop),
                               width=20, height=3)
        submit_button.pack()

    def validate_and_get_data(self, device, temperature, humidity, voltage, entry_start, entry_stop):
        validate = Validator()
        validate_errors = validate.validate_all(device.get(), temperature.get(), humidity.get(), voltage.get(),
                                                entry_start.get(),
                                                entry_stop.get())

        if validate_errors:
            messagebox.showerror('Error', validate_errors)
            return

        df = self.devices.device_probes_from_database(device.get(), temperature.get(), humidity.get(), voltage.get(),
                                                      entry_start.get(), entry_stop.get())
        self.draw_chart(df)

    @staticmethod
    def draw_chart(df):
        if df.empty:
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
        plt.subplots_adjust(hspace=.0)  # remove space between plots
        plt.show()


root = Tk()
app = MainApplication(root)
root.mainloop()
