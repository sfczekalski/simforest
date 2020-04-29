from simforest import SimilarityForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
from scipy.stats import pearsonr
import tqdm


def create_correlated_feature(y, a=10, b=5, fraction=0.2, seed=None, verbose=False):
    """
    Create synthetic column, strongly correlated with target.
    Each value is calculated according to the formula:
        v = y * a + random(-b, b)
        So its scaled target value with some noise.
    Then a fraction of values is permuted, to reduce the correlation.

    Parameters
    ---------
        y : np.ndarray, target vector
        a : int or float (default=10), scaling factor in a formula above
        b : int or float (default=5), value that determines the range of noise to be added
        fraction : float (default=0.2), fraction of values to be permuted to reduce the correlation
        seed : int (default=None), random seed that can be specified to obtain deterministic behaviour
        verbose : bool (default=False), when True, print correlation before and after the shuffling

    Returns
    ----------
        new_column : np.ndarray, new feature vector
        corr : float, correlation of new feature vector with target vector
        p : float, p value of correlation
    """
    if seed is not None:
        np.random.seed(seed)

    new_column = y * a + np.random.uniform(low=-b, high=b, size=len(y))
    if verbose:
        corr, v = pearsonr(new_column, y)
        print(f'Initial new feature - target correlation, without shuffling: {round(corr, 3)}, p: {round(v, 3)}')

    # Choose which samples to permute
    indices = np.random.choice(range(len(y)), int(fraction * len(y)))

    # Find new order of this samples
    shuffled_indices = np.random.permutation(len(indices))
    new_column[indices] = new_column[indices][shuffled_indices]
    corr, p = pearsonr(new_column, y)
    if verbose:
        print(f'New feature - target correlation, after shuffling: {round(corr, 3)}, p: {round(v, 3)}')

    return new_column, corr, p


def importance(model, X, y):
    """
    Measure permutation importance of features in a dataset, according to a given model.
    Returns
    -------
    dictionary with permutation importances
    index of features, from most to least important
    """
    result = permutation_importance(model, X, y, n_repeats=10, random_state=42, n_jobs=4)
    sorted_idx = result.importances_mean.argsort()

    return result, sorted_idx


def get_permutation_importances(rf, sf, X_train, y_train, X_test, y_test, corr=None, labels=None, plot=False):
    """
    Measure permutation features importances according to two models, on both train and test set
    :param rf: first model, already fitted
    :param sf: second model, already fitted
    :param X_train: training dataset
    :param y_train: training labels
    :param X_test: test dataset
    :param y_test: test labels
    :param corr: correlation of new feature with target, used only for plot's legend
    :param labels: name of features in the datasets, used only for plot's legend
    :param plot: bool, whenever to plot the feature importances boxplots or not

    :return:
    dictionary with four values, each with  new feature importances according to a model, on certain dataset
    """

    # Get feature importances for both training and test set
    rf_train_result, rf_train_sorted_idx = importance(rf, X_train, y_train)
    rf_test_result, rf_test_sorted_idx = importance(rf, X_test, y_test)
    sf_train_result, sf_train_sorted_idx = importance(sf, X_train, y_train)
    sf_test_result, sf_test_sorted_idx = importance(sf, X_test, y_test)

    if plot:
        fig, ax = plt.subplots(2, 2, figsize=(14, 8))
        ax[0, 0].set_xlim(-0.05, 0.5)
        ax[0, 0].boxplot(rf_train_result.importances[rf_train_sorted_idx].T,
                         vert=False, labels=labels[rf_train_sorted_idx])
        ax[0, 0].set_title('Random Forest, train set')
        ax[0, 1].set_xlim(-0.05, 0.5)
        ax[0, 1].boxplot(rf_test_result.importances[rf_test_sorted_idx].T,
                         vert=False, labels=labels[rf_test_sorted_idx])
        ax[0, 1].set_title('Random Forest, test set')

        ax[1, 0].set_xlim(-0.05, 0.5)
        ax[1, 0].boxplot(sf_train_result.importances[sf_train_sorted_idx].T,
                         vert=False, labels=labels[sf_train_sorted_idx])
        ax[1, 0].set_title('Similarity Forest, train set')
        ax[1, 1].set_xlim(-0.05, 0.5)
        ax[1, 1].boxplot(sf_test_result.importances[sf_test_sorted_idx].T,
                         vert=False, labels=labels[sf_test_sorted_idx])
        ax[1, 1].set_title('Similarity Forest, test set')
        plt.suptitle(f'Feature importances, correlation: {round(corr, 3)}', fontsize=16)
        plt.show()

    # Return importance of new feature (it's first in the list)
    results = {'rf_train': rf_train_result['importances_mean'][0],
               'rf_test': rf_test_result['importances_mean'][0],
               'sf_train': sf_train_result['importances_mean'][0],
               'sf_test': sf_test_result['importances_mean'][0]}

    return results


def score_model(model, X_train, y_train, X_test, y_test):
    """
    Fit the model on train set and score it on test set.
    Handy function to avoid some duplicated code.
    """
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    score = f1_score(y_test, y_pred)
    return model, score


def bias_experiment(df, y, fraction_range, SEED=None):
    """
    Conduct a experiment, measuring how Random Forest and Similarity Forest compare,
    if a biased column is added to a dataset.

    At each step of this simulation, a new feature is generated using create_correlated_feature function.
    A fraction of this feature values gets shuffled to reduce the correlation.
    During whole experiment, a new features varies from very correlated (biased) feature to completely random.
    Random Forest and Similarity Forest scores and permutation feature importances are measured,
    to asses, how both models are robust to bias present in the dataset.


    :param df: pandas DataFrame with the dataset
    :param y: vector with labels
    :param fraction_range:
    :param SEED: random number generator seed
    :return:
    """
    correlations = np.zeros(len(fraction_range), dtype=np.float32)
    rf_scores = np.zeros(len(fraction_range), dtype=np.float32)
    sf_scores = np.zeros(len(fraction_range), dtype=np.float32)
    permutation_importances = []

    for i, f in tqdm.tqdm(enumerate(fraction_range)):
        # Pop old values
        if 'new_feature' in df.columns:
            df.pop('new_feature')

        # Add new
        new_feature, correlations[i], _ = create_correlated_feature(y, fraction=f, seed=SEED)
        df = pd.concat([pd.Series(new_feature, name='new_feature'), df], axis=1)

        # Split the data with random seed
        X_train, X_test, y_train, y_test = train_test_split(
            df, y, test_size=0.3, random_state=SEED)

        # Preprocess
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Score
        rf, rf_scores[i] = score_model(RandomForestClassifier(random_state=SEED),
                                       X_train, y_train, X_test, y_test)

        sf, sf_scores[i] = score_model(SimilarityForestClassifier(n_estimators=100, random_state=SEED),
                                       X_train, y_train, X_test, y_test)

        # Measure features importances
        permutation_importances.append(get_permutation_importances(rf, sf, X_train, y_train, X_test, y_test))

    return correlations, rf_scores, sf_scores, permutation_importances

