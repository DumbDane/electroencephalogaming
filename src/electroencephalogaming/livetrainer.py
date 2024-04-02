from numpy import mean, std, where
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
import numpy as np
from pandas import DataFrame


class LiveTrainer:
    def __init__(
        self,
        features: list[str],
        classes: list[str],
        markers: list[str],
        clf: LDA,
        mt: float,
        uxt: float,
        ttrials: int,
    ):
        """Create a new LiveTrainer
        >>> features: list of feature names
        >>> classes: list of classes
        >>> classifier: classifier used in predictions
        >>> mt: local machine timestamp when class initialised
        >>> uxt: unix timestamp (s) since class initialised
        >>> trials: total number of trials in experiment
        """

        self.features = features
        self.classes = classes
        self.markers = markers
        self.clf = clf
        self.mt = mt
        self.uxt = uxt
        self.ttrials = ttrials

        # TODO: figure out whether this needs to be separated by classes
        self.smpl_mean = {
            direction: {feature: 0 for feature in self.features}
            for direction in self.classes
        }
        self.smpl_sd = {
            direction: {feature: 0 for feature in self.features}
            for direction in self.classes
        }

    def is_outlier(self, new_features, y):
        for i, ft_name in enumerate(self.features):
            lower, upper = (
                self.smpl_mean[y][ft_name] - self.smpl_sd[y][ft_name],
                self.smpl_mean[y][ft_name] + self.smpl_sd[y][ft_name],
            )
            if new_features[i] < lower or new_features[i] > upper:
                return True
        return False

    def update_mean_sd(self, features, i, labels):
        for cls in self.classes:
            msk = where(labels == cls, labels, False)[:i]
            for j, ftn in enumerate(self.features):
                self.smpl_mean[cls][ftn] = mean(features[j][:i][msk > 0])
                self.smpl_sd[cls][ftn] = std(features[j][:i][msk > 0])

    # should return a np.array of shape 6, with numbers that are voltages
    def get_features():
        ...  # TODO how do we get individual features, can we maybe just read them out from the og data, remember to average over timeframe

    def fit(self, df: DataFrame, samples_seen: int) -> None:
        seen90, seen180, seen270 = df["direction"].value_counts().sort_index()
        initial_trained = False

        labels = np.empty((self.ttrials))  # directions
        c3_alpha = np.empty((self.ttrials))
        c3_beta = np.empty((self.ttrials))
        cz_alpha = np.empty((self.ttrials))
        cz_beta = np.empty((self.ttrials))
        c4_alpha = np.empty((self.ttrials))
        c4_beta = np.empty((self.ttrials))

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

        new_y = df.pop("direction")
        new_x = df

        print(new_x)
        print(new_y)
        new_features = self.get_features()
        if samples_seen > 10:
            if self.is_outlier(new_features, smpl_mean, smpl_sd, new_y):  # noqa
                # TODO: does this make sense for the first ten?
                print("this trial is an outlier and will not be considered")
                return

        for i in range(len(self.features)):
            features[i].append(new_features[i])

        self.smpl_mean, self.smpl_sd = self.update_mean_sd(
            features,
            samples_seen,
            labels,
        )  # noqa

        if not initial_trained:
            if all([seen90, seen180, seen270]) > 10:
                # clf = LinearDiscriminantAnalysis()
                self.clf.fit(features.T, labels)
                initial_trained = True
        else:
            # TODO: add a selection process that gets the best x value
            pred_y = self.clf.predict(new_x)  # noqa
            # TODO: figure out if we can show this prediction on screen somehow or in general what to do with it

            # TODO: add weights
            if all([seen90, seen180, seen270]) > 5:
                # clf = LinearDiscriminantAnalysis()
                self.clf.fit(features.T, labels)
