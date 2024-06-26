from typing import Any
from pylsl import StreamInfo, StreamOutlet
import time
from numpy.random import rand
import numpy as np
import argparse
# from moabb.datasets import BNCI2015_001
# from moabb.paradigms import MotorImagery


def setup(args: argparse.Namespace) -> StreamOutlet:
    participant_id = args.participant_id

    # channel_names = ["participant_id", "start_timestamp_local", "timestamp_local"]
    info = StreamInfo(
        name="electroencephalogaming",
        type=args.type,
        channel_count=args.channel_count,
        nominal_srate=100,
        channel_format="double64",
        source_id=f"electroencephalogaming_{participant_id}",
    )

    info.desc().append_child_value("participant_id", f"{participant_id}")
    info.desc().append_child_value("manufacturere", "brAIn lab")

    chns = info.desc().append_child("channels")
    for label in [
        "C3",
        "C4",
        "Cz",
        "FC3",
        "C5",
        "CP3",
        "C1",
        "FCz",
        "CPz",
        "C2",
        "FC4",
        "CP4",
        "C6",
    ]:  # figure out if order matters # Doesn't if we don't use the script other than testing
        ch = chns.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "EEG")

    # TODO: change this
    cap = info.desc().append_child("cap")
    cap.append_child_value("name", "Enobio8")
    cap.append_child_value("size", "54")
    cap.append_child_value("labelscheme", "10-20")

    print(info.as_xml())
    outlet = StreamOutlet(info)
    return outlet


def get_chunk_from_eeg() -> tuple[np.ndarray, float]:
    return rand(8, 1), time.monotonic()
    ...  # TODO


def push(outlet: StreamOutlet, data, timestamp) -> None:
    outlet.push_sample(data, timestamp)


def main(args: list[str, Any]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, default="EEG", help="Type of stream")
    parser.add_argument(
        "-id",
        "--participant_id",
        type=int,
        required=False,
        default=1,
        help="ID of participant",
    )
    parser.add_argument(
        "--cap_name", type=str, default="Enobio 8", help="Name of EEG cap being used"
    )
    parser.add_argument(
        "-s", "--srate", type=int, default=100, help="Nominal sendrate of EEG (Hz)"
    )
    parser.add_argument(
        "-c",
        "--channel_count",
        type=int,
        default=8,
        help="Number of channels for current recording",
    )

    args, _ = parser.parse_known_args()
    outlet = setup(args)
    # X, labels, meta = MotorImagery().get_data(dataset=BNCI2015_001(), subjects=[1])

    print("now sending data...")
    while True:
        # for trial in X:
        #     for j, _ in enumerate(trial[0]):
        #         push(outlet, *get_chunk_from_eeg())
        #         # push(outlet, trial[:, j], time.time())
        # break
        data_chunk, stamp = get_chunk_from_eeg()
        push(outlet, data_chunk, stamp)
        print("\r", len(data_chunk), end="")
        time.sleep(1 / 500)


if __name__ == "__main__":
    from sys import argv

    main(argv)
