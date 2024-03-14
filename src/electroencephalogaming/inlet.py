from time import sleep
from pylsl import StreamInlet, resolve_stream
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from numpy import mean, std
import numpy as np

FEATURE_NAMES = ["c3_alpha", "c3_beta", "cz_alpha", "cz_beta", "c4_alpha", "c4_beta"]
CLASSES = ["90", "180", "270"]


def getInletStreams():
    streams_eeg = resolve_stream("type", "EEG")  # "name", "electroencephalogaming"
    streams_psypy = resolve_stream("type", "Markers")

    inlet_eeg = StreamInlet(streams_eeg[0])
    inlet_psypy = StreamInlet(streams_psypy[0])
    return inlet_eeg, inlet_psypy


def is_outlier(new_features, smpl_mean, smpl_sd, y):
    for i, ft_name in enumerate(FEATURE_NAMES):
        lower, upper = (
            smpl_mean[y][ft_name] - smpl_sd[y][ft_name],
            smpl_mean[y][ft_name] + smpl_sd[y][ft_name],
        )
        if new_features[i] < lower or new_features[i] > upper:
            return True
    return False


# should return a np.array of shape 6, with numbers that are voltages
def get_features(): ...  # TODO how do we get individual features, can we maybe just read them out from the og data, remember to average over timeframe


def update_mean_sd(features, smpl_mean, smpl_sd, i, labels):
    for cls in CLASSES:
        msk = np.where(labels == cls, labels, False)[:i]
        for j, ftn in enumerate(FEATURE_NAMES):
            smpl_mean[cls][ftn] = mean(features[j][:i][msk > 0])
            smpl_sd[cls][ftn] = std(features[j][:i][msk > 0])


def training(inlet_eeg: StreamInlet, inlet_psypy: StreamInlet):
    num_samples_seen = 0
    seen90 = 0
    seen180 = 0
    seen270 = 0
    initial_trained = False

    labels = np.empty((NUM_TRIALS))
    c3_alpha = np.empty((NUM_TRIALS))
    c3_beta = np.empty((NUM_TRIALS))
    cz_alpha = np.empty((NUM_TRIALS))
    cz_beta = np.empty((NUM_TRIALS))
    c4_alpha = np.empty((NUM_TRIALS))
    c4_beta = np.empty((NUM_TRIALS))

    # TODO: figure out whether this needs to be separated by classes
    smpl_mean = {
        "90": {
            "c3_alpha": 0,
            "c3_beta": 0,
            "cz_alpha": 0,
            "cz_beta": 0,
            "c4_alpha": 0,
            "c4_beta": 0,
        },
        "270": {
            "c3_alpha": 0,
            "c3_beta": 0,
            "cz_alpha": 0,
            "cz_beta": 0,
            "c4_alpha": 0,
            "c4_beta": 0,
        },
        "180": {
            "c3_alpha": 0,
            "c3_beta": 0,
            "cz_alpha": 0,
            "cz_beta": 0,
            "c4_alpha": 0,
            "c4_beta": 0,
        },
    }
    smpl_sd = {
        "90": {
            "c3_alpha": 0,
            "c3_beta": 0,
            "cz_alpha": 0,
            "cz_beta": 0,
            "c4_alpha": 0,
            "c4_beta": 0,
        },
        "270": {
            "c3_alpha": 0,
            "c3_beta": 0,
            "cz_alpha": 0,
            "cz_beta": 0,
            "c4_alpha": 0,
            "c4_beta": 0,
        },
        "180": {
            "c3_alpha": 0,
            "c3_beta": 0,
            "cz_alpha": 0,
            "cz_beta": 0,
            "c4_alpha": 0,
            "c4_beta": 0,
        },
    }

    features = np.array(
        [
            c3_alpha,
            c3_beta,
            cz_alpha,
            cz_beta,
            c4_alpha,
            c4_beta,
        ]
    )
    print("now receiving data...")
    while True:
        # TODO: do something with the timestamps
        chunk_eeg, timestamps_eeg = inlet_eeg.pull_chunk()
        chunk_psypy, timestamps_psypy = (
            inlet_psypy.pull_chunk()
        )  # unclear if this is actually where we are pulling from or if it's from a csv file

        new_x, new_y = chunk_eeg, chunk_psypy

        new_features = get_features()
        if is_outlier(new_features, smpl_mean, smpl_sd, new_y):
            # TODO: does this make sense for the first ten?
            print("this trial is an outlier and will not be considered")
            continue
        num_samples_seen += 1
        labels[num_samples_seen] = new_y
        match new_y:
            case "90":
                seen90 += 1
            case "180":
                seen180 += 1
            case "270":
                seen270 += 1

        for i in range(len(FEATURE_NAMES)):
            features[i].append(new_features[i])

        smpl_mean, smpl_sd = update_mean_sd(
            features, smpl_mean, smpl_sd, num_samples_seen, labels
        )

        if not initial_trained:
            if all([seen90, seen180, seen270]) > 10:
                clf = LinearDiscriminantAnalysis()
                clf.fit(features.T, labels)
                initial_trained = True
        else:
            # TODO: add a selection process that gets the best x value
            pred_y = clf.predict(new_x)
            # TODO: figure out if we can show this prediction on screen somehow or in general what to do with it

            # TODO: add weights
            if all([seen90, seen180, seen270]) > 5:
                clf = LinearDiscriminantAnalysis()
                clf.fit(features.T, labels)

        sleep(0.1)


if __name__ == "__main__":
    inlet_eeg, inlet_psypy = getInletStreams()
    global NUM_TRIALS
    NUM_TRIALS = inlet_psypy.info().desc().child_value("num_trials")
    training(inlet_eeg, inlet_psypy)
