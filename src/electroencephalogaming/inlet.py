from time import monotonic, time  # , sleep
from pylsl import StreamInlet, resolve_stream

# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import numpy as np
import pandas as pd
from glob import glob
from argparse import ArgumentParser
# from livetrainer import LiveTrainer

CHANNELS = ["C1", "C2", "C3", "C4", "FC1", "CZ", "FC2", "PZ"]
FEATURE_NAMES = ["c3_alpha", "c3_beta", "cz_alpha", "cz_beta", "c4_alpha", "c4_beta"]

# {'test' : 99, 'exit' : 86, 'cross' : 1, 'cue' : 2, 'arrow' : 3, 'blank' : 4}
MARKERS = ["markers", "direction"]
CLASSES = ["90", "180", "270"]


def get_inlet_streams():
    print("looking for EEG stream")
    [streams_eeg] = resolve_stream("type", "EEG")
    inlet_eeg = StreamInlet(streams_eeg)
    print("found EEG stream")

    print("looking for psychopy stream")
    [streams_psypy] = resolve_stream("source_id", "1991919")
    inlet_psypy = StreamInlet(streams_psypy)
    print("found psychopy stream")

    return inlet_eeg, inlet_psypy


def pull_df(eeg: StreamInlet, psypy: StreamInlet, mt: float, uxt: float) -> pd.DataFrame:
    """Pulls chunks from two streams, merging them into one dataframe with ffilled values"""

    echunk, etimestamps = eeg.pull_chunk()
    pchunk, ptimestamps = psypy.pull_chunk()

    # Since enobio 8 uses machine uptime for timestamps, we convert to unix manually
    etimestamps = np.array(etimestamps) + uxt - mt

    etmp = pd.DataFrame(index=etimestamps, data=echunk, columns=CHANNELS)
    ptmp = pd.DataFrame(index=ptimestamps, data=pchunk, columns=MARKERS)
    tmp = etmp.merge(ptmp, left_index=True, right_index=True, how="outer")  # .ffill()  # Replaces nan values with previous row

    return tmp


def main(pid: str) -> None:
    id = len(glob("eeg_data/*")) // 2

    def save():
        df.to_parquet(f"eeg_data/{pid}{id}.pq")
        df.to_csv(f"eeg_data/{pid}{id}.csv")

    ieeg, ipsypy = get_inlet_streams()
    # pid = int(ipsypy.info().desc().child_value("participant_id"))
    # Used when converting enobio timestamps to unix timestamps
    mt, uxt = monotonic(), time()
    # num_trials = int(ipsypy.info().desc().child_value("num_trials"))

    # lt = LiveTrainer(FEATURE_NAMES, CLASSES, MARKERS, LDA(), mt, uxt, num_trials)
    df = pd.DataFrame(columns=CHANNELS + MARKERS)
    print("now receiving data...")
    acc = 0
    while True:
        try:
            # EEG uses
            tmp = pull_df(ieeg, ipsypy, mt, uxt)
            if not tmp.empty:
                df = pd.concat([df, tmp])  # .ffill()

            # seen = df[df["direction"] == df["markers"]].shape[0]
            df = df.ffill()
            # print(f"\r{seen}", end="")

            # lt.fit(df.copy()[df["markers"] == 3], seen)

            if acc % 20000 == 0:
                df.to_parquet(f"eeg_data/{pid}{id}.pq")
                df.to_csv(f"eeg_data/{pid}{id}.csv")
                acc = 0
            acc += 1
            if 86 in df["markers"]:
                save(df)
                exit(0)

        except Exception as e:
            raise Exception from e


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--participant", "-p", required=True, type=str, help="lab rat id")
    args, unk = argparser.parse_known_args()

    main(args.participant)
