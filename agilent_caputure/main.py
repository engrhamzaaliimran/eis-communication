from measurement import AgilentMeasurement

f = AgilentMeasurement()
f.folder = './data'
# measurement name
f.name = 'Charakterisierung IIS Sensor leer und mit MOF'
# duration in s
f.duration = (17+0.5)*60*60
f.points = 801
# sampletime in s, ToDo: min 500, get_measurement is slow
f.sampletime = 6
# start measurement
f.start()
