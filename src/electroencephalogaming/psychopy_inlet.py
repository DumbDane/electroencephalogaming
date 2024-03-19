from time import sleep
from pylsl import StreamInlet, resolve_stream
import pandas as pd
import numpy as np

def save(df):
    print(f"Saving to psycho_data/{participant}_{session}")
    df.to_parquet(f"psycho_data/{participant}_{session}.pq")
    df.to_csv(f"psycho_data/{participant}_{session}.csv")


streams = resolve_stream("source_id", "1991919") #"name", "electroencephalogaming"

inlet = StreamInlet(streams[0])
participant: str = inlet.info().desc().child_value("participant_id")
session: str = inlet.info().desc().child_value("session_id")
num_trials: str = inlet.info().desc().child_value("num_trials")
total_trials: str = inlet.info().desc().child_value("total_trials")
df = pd.DataFrame(columns=["markers", "direction"])
print("Now receiving data...")
print(f"{participant = }, {session = }, {num_trials = }, {total_trials = }")
while True:
    try:
        chunk, timestamps = inlet.pull_chunk()
        # print(timestamps, chunk)
        # print("=========")
        print(f"Received chunk of size {len(chunk)}")
        if all(99 in sample for sample in chunk):
            continue
        tmp = pd.DataFrame(index=timestamps, data=chunk, columns=df.columns)
        tmp.dropna(inplace=True)
        df = pd.concat([df, tmp])
        if any(86 in sample for sample in chunk):
            save(df)
            exit(0)
        sleep(.1)

    except Exception as e:
        save(df)
        raise Exception from e
    
