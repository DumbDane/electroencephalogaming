from pylsl import StreamInlet, resolve_stream
import pandas as pd
from glob import glob

[streams] = resolve_stream("type", "EEG")  # "name", "electroencephalogaming"


inlet = StreamInlet(streams)
# participant: str = inlet.info().desc().child_value("participant_id")
# session: str = inlet.info().desc().child_value("session_id")
# num_trials: str = inlet.info().desc().child_value("num_trials")
# total_trials: str = inlet.info().desc().child_value("total_trials")
# df = pd.DataFrame(columns=[f"Sensor{i}" for i in range(8)])

setup1 = [
    "C1",
    "C2",
    "C3",
    "C4",
    "FC1",
    "CZ",
    "FC2",
    "PZ",
]  #'ax', 'az', 'ay', 'flags', 'ux']


df = pd.DataFrame(columns=setup1)

print("Now receiving data...")
# print(f"{participant = }, {session = }, {num_trials = }, {total_trials = }")
while True:
    try:
        chunk, timestamps = inlet.pull_chunk()
        # print(timestamps, chunk)
        # print("=========")
        print(f"Received chunk of size {len(chunk)}")
        tmp = pd.DataFrame(index=timestamps, data=chunk, columns=df.columns)
        if not tmp.any().any():
            continue
        tmp.dropna(inplace=True)
        df = pd.concat([df, tmp])
        print(df.tail())

    except KeyboardInterrupt:
        id = len(glob("eeg_data/*")) // 2
        df.to_parquet(f"eeg_data/fakedata{id}.pq")
        df.to_csv(f"eeg_data/fakedata{id}.csv")
        raise KeyboardInterrupt

    except Exception as e:
        raise Exception from e
