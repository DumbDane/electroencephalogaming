from time import sleep
from pylsl import StreamInlet, resolve_stream
import pandas as pd
import numpy as np

streams = resolve_stream("type", "Markers") #"name", "electroencephalogaming"

inlet = StreamInlet(streams[0])
participant: str = inlet.info().desc().child_value("participant_id")
session: str = inlet.info().desc().child_value("session_id")
num_trials: str = inlet.info().desc().child_value("num_trials")
total_trials: str = inlet.info().desc().child_value("total_trials")
df = pd.DataFrame(columns=["markers"])
print("Now receiving data...")
print(f"{participant = }, {session = }, {num_trials = }, {total_trials = }")
while True:
    try:
        chunk, timestamps = inlet.pull_chunk()
        # print(timestamps, chunk)
        # print("=========")
        # print(f"Received chunk of size {len(chunk)}")
        if all(99 in sample for sample in chunk):
            continue
        tmp = pd.DataFrame(index=timestamps, data=chunk, columns=["markers"])
        tmp.dropna(inplace=True)
        df = pd.concat([df, tmp])
        if any(86 in sample for sample in chunk):
            print(f"Saving to data/{participant}_{session}.pq")
            df.to_parquet(f"data/{participant}_{session}.pq")
            exit(0)
        sleep(.1)

    except Exception as e:
        print(f"An error ocurred, saving data/{participant}_{session}.pq...")
        df.to_parquet(f"data/{participant}_{session}.pq")
        raise Exception from e
    
