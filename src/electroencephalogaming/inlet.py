from time import sleep, monotonic, time
from pylsl import StreamInlet, resolve_stream
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import numpy as np
import pandas as pd
from glob import glob
from argparse import ArgumentParser
from livetrainer import LiveTrainer

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
    print("found EEG stream")

    return inlet_eeg, inlet_psypy


def pull_df(eeg: StreamInlet, psypy: StreamInlet, mt: float, ut: float) -> pd.DataFrame:
    """Pulls chunks from two streams, merging them into one dataframe with ffilled values"""

    echunk, etimestamps = eeg.pull_chunk()
    pchunk, ptimestamps = psypy.pull_chunk()

    # Since enobio 8 uses machine uptime for timestamps, we convert to unix manually
    etimestamps = np.array(etimestamps) + ut - mt

    etmp = pd.DataFrame(index=etimestamps, data=echunk, columns=CHANNELS)
    ptmp = pd.DataFrame(index=ptimestamps, data=pchunk, columns=MARKERS)
    tmp = etmp.merge(
        ptmp, left_index=True, right_index=True, how="outer"
    ).ffill()  # Replaces nan values with previous row

    return tmp


def main(pid: str) -> None:
    ieeg, ipsypy = get_inlet_streams()
    # Used when converting enobio timestamps to unix timestamps
    mt, uxt = monotonic(), time()
    num_trials = int(ipsypy.info().desc().child_value("num_trials"))
    df = pd.DataFrame(columns=CHANNELS + MARKERS)
    lt = LiveTrainer(FEATURE_NAMES, CLASSES, MARKERS, LDA(), mt, uxt, num_trials)

    while True:
        try:
            # EEG uses
            print("now receiving data...")
            tmp = pull_df(ieeg, ipsypy, mt)
            df = pd.concat([df, tmp])
            seen = df[df.shift()["direction"] != df["direction"]].count()

            lt.fit(df.copy()[df["markers"] == 3], seen)

            sleep(1)

        except Exception as e:
            id = len(glob("eeg_data/*")) // 2
            df.to_parquet(f"eeg_data/{pid}{id}.pq")
            df.to_csv(f"eeg_data/{pid}{id}.csv")

            raise Exception from e


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--participant", "-p", required=True, type=str)
    args, unk = argparser.parse_known_args()

    main(args.participant)
