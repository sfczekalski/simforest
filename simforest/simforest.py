"""
This is a module implementing Similarity Forest classifier, outlined here: http://saketsathe.net/downloads/simforest.pdf
"""
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.ensemble.forest import ForestClassifier
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted, check_random_state
from sklearn.utils.multiclass import unique_labels


class SimilarityTreeClassifier(BaseEstimator, ClassifierMixin):
    """Similarity Forest classifier implementation based on scikit-learn-contrib project template.
            Parameters
            ----------

            Attributes
            ----------
    """

    def __init__(self, demo_param='demo_param'):
        self.demo_param = demo_param

    def get_depth(self):
        """Returns the depth of the decision tree.
        The depth of a tree is the maximum distance between the root
        and any leaf.
        """
        pass

    def get_n_leaves(self):
        """Returns the number of leaves of the decision tree.
        """
        pass

    def fit(self, X, y):
        """Build a similarity tree classifier from the training set (X, y).
               Parameters
               ----------
               X : array-like or sparse matrix, shape = [n_samples, n_features]
                   The training input samples.
               y : array-like, shape = [n_samples] or [n_samples, n_outputs]
                   The labels.

               Returns
               -------
               self : object
        """
        # Check that X and y have correct shape
        X, y = check_X_y(X, y)
        # Store the classes seen during fit
        self.classes_ = unique_labels(y)

        self.X_ = X
        self.y_ = y
        self.is_fitted_= True
        # Return the classifier
        return self

    def _validate_X_predict(self, X, check_input):
        """Validate X whenever one tries to predict, apply, predict_proba"""
        pass

    def predict(self, X, check_input=True):
        """A reference implementation of a prediction for a classifier.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : ndarray, shape (n_samples,)
            The labels.
        """
        # Check is fit had been called
        check_is_fitted(self, 'is_fitted_')

        # Input validation
        X = check_array(X)

        return np.ones(X.shape[0], dtype=np.int64)

    def predict_proba(self, X, check_input=True):
        """ A reference implementation of a prediction for a classifier.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : ndarray, shape (n_samples,)
            The labels.
        """
        # Check is fit had been called
        check_is_fitted(self, 'is_fitted_')

        # Input validation
        X = check_array(X)

        return np.ones(X.shape[0], dtype=np.float32)

    def predict_log_proba(self, X):
        """Predict class log-probabilities of the input samples X.
        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]
            The input samples.
        Returns
        -------
        p : array of shape = [n_samples, n_classes].
            The class log-probabilities of the input samples.
        """
        proba = self.predict_proba(X)

        return np.log(proba)

    def apply(self, X, check_input=True):
        """Returns the index of the leaf that each sample is predicted as."""
        pass

    def decision_path(self, X, check_input=True):
        """Return the decision path in the tree."""
        pass

    def _prune_tree(self):
        """Prune tree using Minimal Cost-Complexity Pruning."""
        pass

    def cost_complexity_pruning_path(self, X, y, sample_weight=None):
        """Compute the pruning path during Minimal Cost-Complexity Pruning."""
        pass

    @property
    def feature_importances_(self):
        """Return the feature importances."""
        pass


class SimilarityForestClassifier(ForestClassifier):
    """A similarity forest classifier.
        A similarity forest is a meta estimator that fits a number of similarity tree
        classifiers on various sub-samples of the dataset and uses averaging to
        improve the predictive accuracy and control over-fitting.
        The sub-sample size is always the same as the original
        input sample size but the samples are drawn with replacement if
        `bootstrap=True` (default).
        Read more in the :ref:`User Guide <forest>`.
        Parameters
        ----------
        n_estimators : integer, optional (default=100)
            The number of trees in the forest.
            .. versionchanged:: 0.22
               The default value of ``n_estimators`` changed from 10 to 100
               in 0.22.
        criterion : string, optional (default="gini")
            The function to measure the quality of a split. Supported criteria are
            "gini" for the Gini impurity and "entropy" for the information gain.
            Note: this parameter is tree-specific.
        max_depth : integer or None, optional (default=None)
            The maximum depth of the tree. If None, then nodes are expanded until
            all leaves are pure or until all leaves contain less than
            min_samples_split samples.
        min_samples_split : int, float, optional (default=2)
            The minimum number of samples required to split an internal node:
            - If int, then consider `min_samples_split` as the minimum number.
            - If float, then `min_samples_split` is a fraction and
              `ceil(min_samples_split * n_samples)` are the minimum
              number of samples for each split.
            .. versionchanged:: 0.18
               Added float values for fractions.
        min_samples_leaf : int, float, optional (default=1)
            The minimum number of samples required to be at a leaf node.
            A split point at any depth will only be considered if it leaves at
            least ``min_samples_leaf`` training samples in each of the left and
            right branches.  This may have the effect of smoothing the model,
            especially in regression.
            - If int, then consider `min_samples_leaf` as the minimum number.
            - If float, then `min_samples_leaf` is a fraction and
              `ceil(min_samples_leaf * n_samples)` are the minimum
              number of samples for each node.
            .. versionchanged:: 0.18
               Added float values for fractions.
        min_weight_fraction_leaf : float, optional (default=0.)
            The minimum weighted fraction of the sum total of weights (of all
            the input samples) required to be at a leaf node. Samples have
            equal weight when sample_weight is not provided.
        max_features :
        max_leaf_nodes : int or None, optional (default=None)
            Grow trees with ``max_leaf_nodes`` in best-first fashion.
            Best nodes are defined as relative reduction in impurity.
            If None then unlimited number of leaf nodes.
        min_impurity_decrease : float, optional (default=0.)
            A node will be split if this split induces a decrease of the impurity
            greater than or equal to this value.
            The weighted impurity decrease equation is the following::
                N_t / N * (impurity - N_t_R / N_t * right_impurity
                                    - N_t_L / N_t * left_impurity)
            where ``N`` is the total number of samples, ``N_t`` is the number of
            samples at the current node, ``N_t_L`` is the number of samples in the
            left child, and ``N_t_R`` is the number of samples in the right child.
            ``N``, ``N_t``, ``N_t_R`` and ``N_t_L`` all refer to the weighted sum,
            if ``sample_weight`` is passed.
            .. versionadded:: 0.19
        min_impurity_split : float, (default=1e-7)
            Threshold for early stopping in tree growth. A node will split
            if its impurity is above the threshold, otherwise it is a leaf.
            .. deprecated:: 0.19
               ``min_impurity_split`` has been deprecated in favor of
               ``min_impurity_decrease`` in 0.19. The default value of
               ``min_impurity_split`` will change from 1e-7 to 0 in 0.23 and it
               will be removed in 0.25. Use ``min_impurity_decrease`` instead.
        bootstrap : boolean, optional (default=True)
            Whether bootstrap samples are used when building trees. If False, the
            whole datset is used to build each tree.
        oob_score : bool (default=False)
            Whether to use out-of-bag samples to estimate
            the generalization accuracy.
        n_jobs : int or None, optional (default=None)
            The number of jobs to run in parallel.
            `fit`, `predict`, `decision_path` and `apply` are all
            parallelized over the trees.
            ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
            ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
            for more details.
        random_state : int, RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number generator;
            If RandomState instance, random_state is the random number generator;
            If None, the random number generator is the RandomState instance used
            by `np.random`.
        verbose : int, optional (default=0)
            Controls the verbosity when fitting and predicting.
        warm_start : bool, optional (default=False)
            When set to ``True``, reuse the solution of the previous call to fit
            and add more estimators to the ensemble, otherwise, just fit a whole
            new forest. See :term:`the Glossary <warm_start>`.
        class_weight : dict, list of dicts, "balanced", "balanced_subsample" or \
        None, optional (default=None)
            Weights associated with classes in the form ``{class_label: weight}``.
            If not given, all classes are supposed to have weight one. For
            multi-output problems, a list of dicts can be provided in the same
            order as the columns of y.
            Note that for multioutput (including multilabel) weights should be
            defined for each class of every column in its own dict. For example,
            for four-class multilabel classification weights should be
            [{0: 1, 1: 1}, {0: 1, 1: 5}, {0: 1, 1: 1}, {0: 1, 1: 1}] instead of
            [{1:1}, {2:5}, {3:1}, {4:1}].
            The "balanced" mode uses the values of y to automatically adjust
            weights inversely proportional to class frequencies in the input data
            as ``n_samples / (n_classes * np.bincount(y))``
            The "balanced_subsample" mode is the same as "balanced" except that
            weights are computed based on the bootstrap sample for every tree
            grown.
            For multi-output, the weights of each column of y will be multiplied.
            Note that these weights will be multiplied with sample_weight (passed
            through the fit method) if sample_weight is specified.
        ccp_alpha : non-negative float, optional (default=0.0)
            Complexity parameter used for Minimal Cost-Complexity Pruning. The
            subtree with the largest cost complexity that is smaller than
            ``ccp_alpha`` will be chosen. By default, no pruning is performed. See
            :ref:`minimal_cost_complexity_pruning` for details.
            .. versionadded:: 0.22

        Attributes
        ----------
        base_estimator_ : SimilarityTreeClassifier
            The child estimator template used to create the collection of fitted
            sub-estimators.
        estimators_ : list of SimilarityTreeClassifiers
            The collection of fitted sub-estimators.
        classes_ : array of shape = [n_classes] or a list of such arrays
            The classes labels (single output problem), or a list of arrays of
            class labels (multi-output problem).
        n_classes_ : int or list
            The number of classes (single output problem), or a list containing the
            number of classes for each output (multi-output problem).
        n_features_ : int
            The number of features when ``fit`` is performed.
        n_outputs_ : int
            The number of outputs when ``fit`` is performed.
        feature_importances_ :
        oob_score_ : float
            Score of the training dataset obtained using an out-of-bag estimate.
        oob_decision_function_ : array of shape = [n_samples, n_classes]
            Decision function computed with out-of-bag estimate on the training
            set. If n_estimators is small it might be possible that a data point
            was never left out during the bootstrap. In this case,
            `oob_decision_function_` might contain NaN.

        Notes
        -----
        The default values for the parameters controlling the size of the trees
        (e.g. ``max_depth``, ``min_samples_leaf``, etc.) lead to fully grown and
        unpruned trees which can potentially be very large on some data sets. To
        reduce memory consumption, the complexity and size of the trees should be
        controlled by setting those parameter values.
        To obtain a deterministic behaviour during
        fitting, ``random_state`` has to be fixed.
    """
    def __init__(self,
                 n_estimators=100,
                 criterion="gini",
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.,
                 max_features=None,
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.,
                 min_impurity_split=None,
                 bootstrap=True,
                 oob_score=False,
                 n_jobs=None,
                 random_state=None,
                 verbose=0,
                 warm_start=False,
                 class_weight=None,
                 ccp_alpha=0.0):
        super().__init__(
            base_estimator=SimilarityTreeClassifier(),
            n_estimators=n_estimators,
            estimator_params=[],
            bootstrap=bootstrap,
            oob_score=oob_score,
            n_jobs=n_jobs,
            random_state=random_state,
            verbose=verbose,
            warm_start=warm_start,
            class_weight=class_weight)

        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.min_impurity_split = min_impurity_split
        self.ccp_alpha = ccp_alpha


class SimilarityTreeRegressor(BaseEstimator, RegressorMixin):
    """Similarity Tree regressor implementation.
            Similarity Trees are base models used as building blocks for Similarity Forest ensemble.
                Parameters
                ----------
                random_state : int, random numbers generator seed
                n_directions : int, number of discriminative directions to check at each split.
                                   The best direction is chosen, based on child nodes' purity.
                sim_function : function used to measure similarity between data-points
                max_depth : integer or None, optional (default=None)
                    The maximum depth of the tree. If None, then nodes are expanded until
                    all leaves are pure.
                depth : int depth of the tree count

                Attributes
                ----------
                is_fitted_ : bool flag indicating whenever fit has been called
                X_ : data used for fitting the forest
                y_ : training data outputs
                _nodes_list : list of SimilarityTreeClassifier instances, that is tree nodes
                _lhs : SimilarityTreeClassifier current node's left child node
                _rhs : SimilarityTreeClassifier current node's right child node
                _p : first data-point used for drawing split direction in the current node
                _q : second data-point used for drawing split direction in the current node
                _similarities :
                    ndarray of similarity values between two datapoints used for splitting and rest of training datapoints
                _split_point = float similarity value decision boundary
                _value = output value for current node, estimated based on training set
                _is_leaf :
                    bool indicating if current node is a leaf, because stopping createrion
                    has been reached (depth == max_depth)
                _node_id : int current node id

        """

    # List of all nodes in the tree, that is SimilarityTreeClassifier instances. Shared across all instances
    _nodes_list = []

    def __init__(self,
                 random_state=1,
                 n_directions=1,
                 sim_function=np.dot,
                 max_depth=None,
                 depth=1):
        self.random_state = random_state
        self.n_directions = n_directions
        self.sim_function = sim_function
        self.max_depth = max_depth
        self.depth = depth

    def apply(self, X, check_input=False):
        """Returns the index of the leaf that each sample is predicted as."""

        if check_input:
            # Check if fit had been called
            check_is_fitted(self, ['X_', 'y_', 'is_fitted_'])

            # Input validation
            X = check_array(X)

            X = self._validate_X_predict(X, check_input)

    def decision_path(self, X):
        pass

    def get_depth(self):
        """Returns the depth of the decision tree.
        The depth of a tree is the maximum distance between the root
        and any leaf.
        """

        check_is_fitted(self, ['X_', 'y_', 'is_fitted_'])

        if self is None:
            return 0
        elif self._lhs is None and self._rhs is None:
            return 1
        else:
            l_depth = self._lhs.get_depth()
            r_depth = self._rhs.get_depth()

            if l_depth > r_depth:
                return l_depth + 1
            else:
                return r_depth + 1

    def get_n_leaves(self):
        """Returns the number of leaves of the similarity tree.
        """
        if self is None:
            return 0
        if self._lhs is None and self._rhs is None:
            return 1
        else:
            return self._lhs.get_n_leaves() + self._rhs.get_n_leaves()

    def fit(self, X, y, check_input=True):
        """Build a similarity tree regressor from the training set (X, y).
               Parameters
               ----------
               X : array-like of any type, as long as suitable similarity function is provided
                   The training input samples.
               y : array-like, shape = [n_samples]
                   The training outputs.

               Returns
               -------
               self : object
        """

        # Check input
        if check_input:
            # Check that X and y have correct shape
            X, y = check_X_y(X, y)

            # Input validation, check it to be a non-empty 2D array containing only finite values
            X = check_array(X)

            # Check if provided similarity function applies to input
            X = self._validate_X_predict(X, check_input)

        # Check parameters
        random_state = check_random_state(self.random_state)

        self.X_ = X
        self.y_ = y
        self._lhs = None
        self._rhs = None
        self._p = None
        self._q = None
        self._similarities = []
        self._split_point = -np.inf
        self._value = None
        self._is_leaf = False
        self.is_fitted_ = False

        # Append self to the list of class instances
        self._nodes_list.append(self)

        # Current node id is length of all nodes list. Nodes are numbered from 1, the root node
        self._node_id = len(self._nodes_list)

        if self.max_depth is not None:
            if self.depth == self.max_depth:
                self._is_leaf = True
                return self

        self.is_fitted_= True

        return self

    def _validate_X_predict(self, X, check_input):
        """Validate X whenever one tries to predict, apply."""

        X = check_array(X)

        return X

    def predict(self, X, check_input=True):

        if check_input:
            # Check if fit had been called
            check_is_fitted(self, ['X_', 'y_', 'is_fitted_'])

            # Input validation
            X = check_array(X)

            X = self._validate_X_predict(X, check_input)

        return

    @property
    def feature_importances_(self):
        """Return the feature importances."""
        pass

    class SimilarityForestRegressor(BaseEstimator, RegressorMixin):
        """A similarity forest regressor.
                A similarity forest is a meta estimator that fits a number of similarity tree
                regressors on various sub-samples of the dataset and uses averaging to
                improve the predictive accuracy and control over-fitting.
                The sub-sample size is always the same as the original
                input sample size but the samples are drawn with replacement.
                Parameters
                ----------
                random_state : int, RandomState instance or None, optional (default=None)
                    If int, random_state is the seed used by the random number generator;
                    If RandomState instance, random_state is the random number generator;
                    If None, the random number generator is the RandomState instance used
                    by `np.random`.
                n_estimators : integer, optional (default=20)
                    The number of trees in the forest.
                n_directions : int, number of discriminative directions to check at each split.
                                    The best direction is chosen, based on child nodes' purity.
                sim_function : function used to measure similarity between data-points
                max_depth : integer or None, optional (default=None)
                    The maximum depth of the tree. If None, then nodes are expanded until
                    all leaves are pure.
                oob_score : bool (default=False)
                    Whether to use out-of-bag samples to estimate the R^2 on unseen data.

                Attributes
                ----------
                base_estimator_ : SimilarityTreeRegressor
                    The child estimator template used to create the collection of fitted
                    sub-estimators.
                estimators_ : list of SimilarityTreeRegressors
                    The collection of fitted sub-estimators.
                oob_score_ : float
                    Score of the training dataset obtained using an out-of-bag estimate.
                oob_prediction_ :
                    array of shape = [n_samples] Prediction computed with out-of-bag estimate on the training set.
                is_fitted_ : bool flag indicating whenever fit has been called
                X_ : data used for fitting the forest
                y_ : data labels

                Notes
                -----
                The default values for the parameters controlling the size of the trees
                (``max_depth``) lead to fully grown and
                unpruned trees which can potentially be very large on some data sets. To
                reduce memory consumption, the size of the trees should be
                controlled by setting those parameter values.
                To obtain a deterministic behaviour during
                fitting, ``random_state`` has to be fixed.
                """

        def __init__(self,
                     random_state=1,
                     n_estimators=20,
                     n_directions=1,
                     sim_function=np.dot,
                     max_depth=None,
                     oob_score=False):
            self.random_state = random_state
            self.n_estimators = n_estimators
            self.n_directions = n_directions
            self.sim_function = sim_function
            self.max_depth = max_depth
            self.oob_score = oob_score

        def apply(self, X, check_input=False):
            """Returns the index of the leaf that each sample is predicted as."""

            if check_input:
                # Check if fit had been called
                check_is_fitted(self, ['X_', 'y_', 'is_fitted_'])

                # Input validation
                X = check_array(X)

                X = self._validate_X_predict(X, check_input)

        def decision_path(self, X):
            pass

        def fit(self, X, y, check_input=True):
            """Build a similarity forest regressor from the training set (X, y).
                   Parameters
                   ----------
                   X : array-like of any type, as long as suitable similarity function is provided
                       The training input samples.
                   y : array-like, shape = [n_samples]
                       The training outputs.

                   Returns
                   -------
                   self : object
            """

            # Check input
            if check_input:
                # Check that X and y have correct shape
                X, y = check_X_y(X, y)

                # Input validation, check it to be a non-empty 2D array containing only finite values
                X = check_array(X)

                # Check if provided similarity function applies to input
                X = self._validate_X_predict(X, check_input)

            return self

        def _validate_X_predict(self, X, check_input):
            """Validate X whenever one tries to predict, apply."""

            X = check_array(X)

            return X

        def predict(self, X, check_input=True):

            if check_input:
                # Check if fit had been called
                check_is_fitted(self, ['X_', 'y_', 'is_fitted_'])

                # Input validation
                X = check_array(X)

                X = self._validate_X_predict(X, check_input)

            return

        @property
        def feature_importances_(self):
            """Return the feature importances."""
            pass
