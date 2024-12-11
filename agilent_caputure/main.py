from datetime import datetime
from measurement import AgilentMeasurement

# Create the AgilentMeasurement instance
f = AgilentMeasurement()
f.folder = './data'

# Get the current date and time
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Measurement name with current date and time
f.name = str(current_time)

# Duration in seconds
# f.duration = 10*100 #(17 + 0.5) * 5

# Number of points
f.points = 801

# Sample time in seconds (ToDo: minimum 500, get_measurement is slow)
f.sampletime = 100
f.duration = 10*f.sampletime #(17 + 0.5) * 5

# Start the measurement
f.start()