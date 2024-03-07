from time import sleep
from pylsl import StreamInlet, resolve_stream

streams = resolve_stream("type", "EEG") #"name", "electroencephalogaming"

inlet = StreamInlet(streams[0])


print("now receiving data...")
while True:
    chunk, timestamps = inlet.pull_chunk()
    print(timestamps, chunk)
    sleep(0.1)
    

