# Adapted from "decoding_csp_eeg.ipynb" by Martin Billinger <martin.billinger@tugraz.at>
#
# License: BSD-3-Clause
# Copyright the MNE-Python contributors.


from typing import Callable
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from glob import glob

from sklearn.svm import SVC
from sklearn.model_selection import ShuffleSplit, cross_val_score
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, make_scorer, confusion_matrix

from mne import Epochs, pick_types, find_events
from mne.channels import make_standard_montage
from mne.decoding import CSP, UnsupervisedSpatialFilter, Vectorizer, Scaler
from mne.io import concatenate_raws, read_raw_fif, Raw  # , read_raw_edf

from argparse import ArgumentParser


def load_raw(pathglob: str, read_raw_func: Callable = read_raw_fif, **kwargs):
    """
    Uses glob pattern to read and concatenate raw files.

    >>> pathglob      : glob pattern used to find raw files
    >>> read_raw_func : mne io function used to read globbed files
    *
    >>> kwargs        : montage : str, default standard_1005
    """

    raw_fnames = glob(pathglob)
    raw = concatenate_raws([read_raw_func(f, preload=True) for f in raw_fnames])

    montage = make_standard_montage(kwargs.get("montage", "standard_1005"))
    raw.set_montage(montage)
    raw.set_eeg_reference(projection=True)
    raw.apply_proj()

    # Apply band-pass filter
    raw.filter(7.0, 30.0, fir_design="firwin", skip_by_annotation="edge")

    return raw


def load_epochs(raw: Raw, classes: list[str]):
    """
    Load epochs from the given raw
    >>> raw    : MNE Raw object
    """
    # *
    # >>> kwargs : tmin    : int, default -1
    #              tmax    : int, default 4
    # """

    # #############################################################################
    # # Set parameters and read data

    # avoid classification of evoked responses by using epochs that start 1s after
    # cue onset.
    tmin, tmax = -1.0, 4

    picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude="bads")
    events = find_events(raw, stim_channel="trigger", verbose=True)

    # Read epochs (train will be done only between 1 and 2s)
    # Testing will be done with a running classifier
    epochs = Epochs(
        raw,
        events=events,
        event_id=classes,
        tmin=tmin,
        tmax=tmax,
        proj=True,
        picks=picks,
        baseline=None,
        preload=True,
    )

    return epochs


def train(epochs_train: Epochs, labels: list[str]):
    true_classes, pred_classes = [], []

    def classification_report_with_accuracy_score(y_true, y_pred):
        # print(classification_report(y_true, y_pred)) # print classification report
        true_classes.extend(y_true)
        pred_classes.extend(y_pred)
        return accuracy_score(y_true, y_pred)  # return accuracy score

    # Define a monte-carlo cross-validation generator (reduce variance):
    scores = []
    epochs_data = epochs_train.get_data(copy=False)
    cv = ShuffleSplit(10, test_size=0.2, random_state=42)

    # Preprocessing
    scaler = Scaler(epochs_train.info)
    # csp = CSP(n_components=8, reg=None, norm_trace=False, log=True)
    pca = UnsupervisedSpatialFilter(PCA(), average=False)
    vec = Vectorizer()

    # Assemble a classifier
    # lda = LinearDiscriminantAnalysis()
    svc = SVC(kernel="linear")

    # Use scikit-learn Pipeline with cross_val_score function
    # clf = Pipeline([("PCA", pca), ("CSP", csp), ("LDA", lda)])
    # clf = Pipeline([("Scaler", scaler), ("PCA", pca), ("Vectorizer", vec), ("LDA", lda)])
    clf = Pipeline([("Scaler", scaler), ("PCA", pca), ("Vectorizer", vec), ("SVM", svc)])

    scores = cross_val_score(
        clf, epochs_data, labels, cv=cv, n_jobs=None, scoring=make_scorer(classification_report_with_accuracy_score)
    )
    # scores = cross_val_score(clf, epochs, labels, cv=cv, n_jobs=None)

    # Printing the results
    # class_balance = np.mean(labels == labels[0])
    # class_balance = max(class_balance, 1.0 - class_balance)
    # print(f"Classification accuracy: {np.mean(scores)} / Chance level: {class_balance}")

    # plot CSP patterns estimated on full data for visualization
    # csp.fit_transform(epochs_data, labels)

    # csp.plot_patterns(epochs.info, ch_type="eeg", units="Patterns (AU)", size=1.5)
    # Printing the results

    return true_classes, pred_classes, scores, cv


def plot_cf(
    cf: np.ndarray[np.ndarray[int]], title: str, classes: list[str | int], label_convert: dict[str | int, str] = None, **kwargs
):
    """
    Plots confusion matrix for a given classifier

    >>> cf            : Confusion matrix (shaped like output of sklearn.metrics confusion matrix)
    >>> title         : Plot title
    >>> classes       : List of class identifiers
    >>> label_convert : Map between class identifier and their string representation
    *
    >>> kwargs        : cmap : sns cmap palette
    """
    cmap = kwargs.get("cmap", sns.light_palette("#69B45B", as_cmap=True))
    savefigs = False
    font = {"size": 12}
    label_convert = label_convert or {90: "Right", 180: "Feet", 270: "Left"}

    group_names = [
        x
        for xs in [["True " + label_convert[c] if c == i else "False " + label_convert[c] for c in classes] for i in classes]
        for x in xs
    ]
    # creating labels to add to the heatmap
    # group_names = ['True Pop','False Rap','False Rb',
    #                'False Pop', 'True Rap', 'False Rb',
    #                'False Pop', 'False Rap', 'True Rb']
    group_counts = ["{0:0.0f}".format(value) for value in cf.flatten()]
    labels = [f"{v1}\n{v2}" for v1, v2 in zip(group_names, group_counts)]
    labels = np.asarray(labels).reshape(len(classes), len(classes))
    print(labels)

    # creating the heatmap and adding titels
    f, ax = plt.subplots(figsize=(10, 7))
    ticks = [label_convert[c] for c in classes]
    sns.heatmap(cf, annot=labels, fmt="", cmap=cmap, xticklabels=ticks, yticklabels=ticks, ax=ax)

    ax.set_xlabel("Predicted", fontdict=font)
    ax.set_ylabel("Actual", fontdict=font)

    plt.suptitle(title, fontsize=18, x=0.45)
    plt.title("Heatmap of the confusion matrix", fontsize=12)
    plt.show(block=True)
    if savefigs:
        plt.savefig(f"figs/cf_{title}.png", bbox_inches="tight")


def plot_sliding_window(
    cv: ShuffleSplit, epochs_full, epochs_train: Epochs, classes: list[str | int], labels: list[str | int], sfreq
):
    """
    Plot sliding window graph for a PCA |> CSP |> SVC pipeline.

    >>> cv           : Preinitialised sklearn ShuffleSplit object used for crossvalidation training
    >>> epochs_train : Epochs cropped to time frame of interest
    >>> classes      : List of class identifiers
    >>> labels       : List of labels corresponding to the training data
    >>> sfreq        : Sampling frequency for raws
    """

    assert len(classes) < 3, "Can't do CSP on more than 2 classes"
    epochs_full_data = epochs_full.get_data(copy=False)
    epochs_train_data = epochs_train.get_data(copy=False)
    cv_split = cv.split(epochs_train_data)
    w_length = int(sfreq * 0.5)  # running classifier: window length
    w_step = int(sfreq * 0.1)  # running classifier: window step size
    w_start = np.arange(0, epochs_full_data.shape[2] - w_length, w_step)

    scores_windows = []

    # minipca = Pipeline([("PCA", PCA()), ("Vectorizer", Vectorizer())])
    minicsp = Pipeline([("PCA", UnsupervisedSpatialFilter(PCA())), ("CSP", CSP())])
    svc = SVC(random_state=42)

    for train_idx, test_idx in cv_split:
        y_train, y_test = labels[train_idx], labels[test_idx]

        X_train = minicsp.fit_transform(epochs_train_data[train_idx], y_train)
        X_test = minicsp.transform(epochs_train_data[test_idx])
        # fit classifier
        svc.fit(X_train, y_train)

        # running classifier: test classifier on sliding window
        score_this_window = []
        for n in w_start:
            X_test = minicsp.transform(epochs_full_data[test_idx][:, :, n : (n + w_length)])
            score_this_window.append(svc.score(X_test, y_test))

        scores_windows.append(score_this_window)

    # Plot scores over time
    w_times = (w_start + w_length / 2.0) / sfreq + epochs_full.tmin
    plt.figure()
    plt.plot(w_times, np.mean(scores_windows, 0), label="Score")
    plt.axvline(0, linestyle="--", color="k", label="Onset")
    plt.axhline(0.5, linestyle="-", color="k", label="Chance")
    plt.ylim(bottom=0, top=1)
    plt.xlabel("time (s)")
    plt.ylabel("classification accuracy")
    plt.title("Classification score over time")
    plt.legend(loc="lower right")
    plt.show(block=True)


def main(tmin: float, tmax: float, classes: list[str | int], subject: str, session: str, **kwargs):
    path = f"data/scratch/{subject}/{session}/**raw.fif"

    raw = load_raw(path, **kwargs)
    epochs_full = load_epochs(raw, classes=classes, **kwargs)
    labels = epochs_full.events[:, -1]

    epochs_train = epochs_full.copy().crop(tmin=tmin, tmax=tmax, verbose=False)

    tc, pc, scores, cv = train(epochs_train, labels)

    title = f"Motor Imagery for {len(classes)} classes"
    plot_cf(confusion_matrix(tc, pc), title, classes)
    class_balance = np.mean(labels == labels[0])
    class_balance = min(class_balance, 1.0 - class_balance)
    print(classification_report(pc, tc))  # print classification report
    print("=" * 20)
    print(f"Classification accuracy: {np.mean(scores)} / Chance level: {class_balance}")
    if len(classes) < 3:
        sfreq = raw.info["sfreq"]

        plot_sliding_window(cv, epochs_full, epochs_train, classes, labels, sfreq)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--tmin", type=float, help="tmin for load_epochs function")
    parser.add_argument("--tmax", type=float, help="tmax for load_epochs function")
    parser.add_argument("--classes", "-c", default=[90, 180, 270], type=int, nargs="*")

    parser.add_argument("--participant", "-p", dest="subject", required=True, type=str)
    parser.add_argument("--session", "-s", type=str, default="*")

    args, unk = parser.parse_known_args()

    main(**vars(args))
