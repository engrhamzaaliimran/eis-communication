import h5py
import os
import time
import threading
import datetime
import numpy as np
from tabulate import tabulate
import pyvisa as visa
import scipy.io as scio
from timer import Timer


class AgilentMeasurement:
    def __init__(self):
        self.name = 'test'
        self.folder = None
        self._last_id = 0
        self._timer = None
        self.duration = None
        self.sampletime = 1000
        self._start_time = time.perf_counter()
        self.instrument = None
        self._filename = None
        self.initialize()
        self.points = None

    def initialize(self):
        rm = visa.ResourceManager()
        instrument_list = rm.list_resources()
        self.instrument = rm.open_resource(instrument_list[6])
        devicename = self.instrument.query('*IDN?')
        print(devicename)
        self.instrument.write('ESNB 1')
        self.instrument.write('*SRE 4')
        self.instrument.write('*CLS')
        bla = self.instrument.query('*OPC?')

    @property
    def remaining_time(self):
        return self.duration - self.elapsed_time if self.duration is not None else None

    @property
    def elapsed_time(self):
        return time.perf_counter()-self._start_time

    def create_file(self):
        now = datetime.datetime.now()
        self._filename = self.folder + '/' + now.strftime("%Y%m%d_%H%M%S") + "_" + self.name + '.h5'
        if self._filename is None:
            return None
        directory = os.path.dirname(os.path.abspath(self._filename))
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Creating directory: %s." % directory)
            return None
        file = h5py.File(self._filename, 'w', libver='earliest')
        file.create_dataset('magnitude', dtype=np.float64, shape=(0, self.points), maxshape=(None, self.points), chunks=(1, self.points),
                            compression="gzip", compression_opts=9)
        file.create_dataset('phase', dtype=np.float64, shape=(0, self.points), maxshape=(None, self.points), chunks=(1, self.points),
                            compression="gzip", compression_opts=9)
        file.create_dataset('frequency', dtype=np.float64, shape=(0, self.points), maxshape=(None, self.points), chunks=(1, self.points),
                            compression="gzip", compression_opts=9)
        file.create_dataset('timestamp', dtype=np.uint64, shape=(0, 1), maxshape=(None, 1), chunks=(10, 1),
                            compression="gzip", compression_opts=9)
        file.close()
        return None

    def get_measurement(self):
        i=0
        frequencies = self.instrument.query('OUTPSWPRM?').replace('\n', '').split(',')
        self.instrument.write('SING')
        self.instrument.write('*TRG')
        timestamp = datetime.datetime.timestamp(datetime.datetime.now())
        while int(self.instrument.query('*STB?')) is not 68:
            #blub = self.instrument.query('*STB?')
            time.sleep(1)
            i = i + 1
            if i > self.sampletime:
                break

        impedance = self.instrument.query('OUTPDATA?').replace('\n', '').split(',')
        self.instrument.write('*CLS')
        bla = self.instrument.query('*OPC?')
        real_part = np.array(impedance[0::2],dtype=np.float64)
        imag_part = np.array(impedance[1::2],dtype=np.float64)
        magnitude = np.sqrt(real_part**2+imag_part**2)
        phase = np.arctan2(imag_part,real_part)
        return {'frequency': np.array(frequencies,dtype=np.float64), 'magnitude': magnitude, 'phase': phase, 'timestamp': timestamp}

    def measurement(self):
        mea = self.get_measurement()
        file = h5py.File(self._filename, 'r+')
        file['magnitude'].resize(file['magnitude'].shape[0] + 1, axis=0)
        file['phase'].resize(file['phase'].shape[0] + 1, axis=0)
        file['frequency'].resize(file['frequency'].shape[0] + 1, axis=0)
        file['timestamp'].resize(file['timestamp'].shape[0] + 1, axis=0)


        file['frequency'][-1, :] = mea['frequency'][0:]
        file['phase'][-1, :] = mea['phase'][0:]
        file['magnitude'][-1, :] = mea['magnitude'][0:]
        file['timestamp'][-1] = mea['timestamp']
        file.flush()
        file.close()

    def read_user_commands(self):
        supported_commands = [
            ('progress', 'p',
             'Print progress information'),
            ('abort', 'a',
             'Abort measurement'),
            ('id', 'i',
             'Latest id')
        ]
        data = tabulate(tabular_data=supported_commands, tablefmt="fancy_grid")
        print('The following commands are supported:\n{}'.format(data))
        while True:
            cmd = input()
            if len(cmd) == 0:
                continue
            elif cmd in ['a', 'abort']:
                print("Aborted by user.")
                self.stop()
            elif cmd in ['p', 'progress']:
                if self.duration is None:
                    print("time elapsed: {:.1f} s, duration: ∞".format(
                          self.elapsed_time))
                else:
                    print("time elapsed: {:.1f} s, time remaining: {:.1f} s, duration: {:.1f} s".format(
                          self.elapsed_time, self.remaining_time, self.duration))
            elif cmd in ['i', 'id']:
                print("latest id: {}".format(self._last_id))
            else:
                print("No such command: " + cmd)

    def timer(self):
        self._start_time = time.perf_counter()
        while self.elapsed_time < self.duration:
            time.sleep(0.1)
        self.stop()

    def start(self):
        self.create_file()
        self._timer = Timer(self.sampletime, self.measurement)
        threading.Thread(target=self.read_user_commands, daemon=True).start()
        if self.duration is not None:
            threading.Thread(target=self.timer, daemon=True).start()
        self._timer.start()

    def stop(self):
        self._timer.stop()


