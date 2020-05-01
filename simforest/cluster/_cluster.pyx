# from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
# https://cython.readthedocs.io/en/latest/src/tutorial/memory_allocation.html
import numpy as np
cimport numpy as np
cimport cython
from scipy.special import comb
from sklearn.utils.validation import check_random_state
from cython.parallel import prange, parallel
cimport openmp
from libc.math cimport exp


# projection function type definition
ctypedef float (*f_type)(float [:] xi, float [:] p, float [:] q) nogil
"""This type represents a function type for a function that calculates projection of data-points on split direction.
    Parameters
    ----------
        xi : memoryview of ndarray, a data-point to be projected
        p : memoryview of ndarray, first data-point used for drawing split direction
        q : memoryview of ndarray, second data-point used for drawing split direction
    Returns 
    ----------
        float, value of projection on given split direction
"""


@cython.boundscheck(False)
@cython.wraparound(False)
cdef float dot(float [:] u, float [:] v) nogil:
    """Calcuate dot product of two vectors.
        Parameters
        ----------
            u : memoryview of ndarray, first vector
            v : memoryview of ndarray, second vector
        Returns 
        ----------
            result : float value
    """
    cdef float result = 0.0
    cdef int n = u.shape[0]
    cdef int i = 0
    for i in range(n):
        result += u[i] * v[i]

    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline float dot_projection(float [:] xi, float [:] p, float [:] q) nogil:
    """Projection of data-point on split direction using dot product.
        Parameters
        ----------
            xi : memoryview of ndarray, data-point to be projected
            p : memoryview of ndarray, first data-point used to draw split direction
            q : memoryview of ndarray, second data-point used to draw split direction
        Returns 
        ----------
            result : float value
    """
    cdef float result = 0.0
    cdef int n = xi.shape[0]
    cdef int i = 0
    cdef float q_p

    for i in range(n):
        q_p = q[i] - p[i]
        result += xi[i] * q_p

    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cdef float sqeuclidean(self, float [:] u, float [:] v) nogil:
    """Calcuate squared euclidean distance of two vectors. 
        It serves as an approximation of euclidean distance, when sorted using both methods, 
        the order of data-points remains the same. 
        Parameters
        ----------
            u : memoryview of ndarray, first vector
            v : memoryview of ndarray, second vector
        Returns 
        ----------
            result : float value
    """
    cdef float result = 0.0
    cdef int n = u.shape[0]
    cdef int i = 0
    for i in range(n):
        result += (u[i] - v[i]) ** 2

    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline float sqeuclidean_projection(float [:] xi, float [:] p, float [:] q) nogil:
    """Projection of data-point on split direction using squared euclidean distance.
        It serves as an approximation of euclidean distance, when sorted using both methods, 
        the order of data-points remains the same. 
        Parameters
        ----------
            xi : memoryview of ndarray, data-point to be projected
            p : memoryview of ndarray, first data-point used to draw split direction
            q : memoryview of ndarray, second data-point used to draw split direction
        Returns 
        ----------
            result : float value
    """
    cdef float result = 0.0
    cdef int n = xi.shape[0]
    cdef int i = 0
    cdef float p_q

    for i in range(n):
        p_q = p[i] - q[i]
        result += xi[i] * p_q

    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline float rbf_projection(float [:] xi, float [:] p, float [:] q) nogil:
    """Projection of data-point on split direction using squared euclidean distance.
        It serves as an approximation of euclidean distance, when sorted using both methods, 
        the order of data-points remains the same. 
        Parameters
        ----------
            xi : memoryview of ndarray, data-point to be projected
            p : memoryview of ndarray, first data-point used to draw split direction
            q : memoryview of ndarray, second data-point used to draw split direction
        Returns 
        ----------
            result : float value
    """
    cdef float result = 0.0
    cdef float xq = 0.0
    cdef float xp = 0.0
    cdef int n = xi.shape[0]
    cdef float gamma = 1 / <float>len(xi)
    cdef int i = 0
    cdef float temp_x_q
    cdef float temp_x_p

    for i in range(n):
        temp_x_q = xi[i] - q[i]
        xq += temp_x_q ** temp_x_q

        temp_x_p = xi[i] - p[i]
        xp += temp_x_p ** temp_x_p

    xq = exp(-gamma * xq)
    xp = exp(-gamma * xp)

    result = xq - xp

    return result

cdef class CSimilarityForestClusterer:
    """Similarity forest clusterer."""

    cdef random_state
    cdef str sim_function
    cdef int max_depth
    cdef public list estimators_
    cdef int n_estimators
    cdef int bootstrap

    def __cinit__(self,
                  random_state=None,
                  str sim_function='euclidean',
                  int max_depth=-1,
                  int n_estimators = 20,
                  int bootstrap = 0):
        self.random_state = random_state
        self.sim_function = sim_function
        self.max_depth = max_depth
        self.estimators_ = []
        self.n_estimators = n_estimators
        self.bootstrap = bootstrap

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef CSimilarityForestClusterer fit(self, np.ndarray[np.float32_t, ndim=2] X):
        """Build a forest of trees from the training set X.
            Parameters
            ----------
            X : array-like matrix of shape = [n_samples, n_features]
                The training data samples.
            Returns
            -------
            self : CSimilarityForestClusterer
        """
        cdef int n = X.shape[0]
        cdef dict args = dict()

        cdef random_state = check_random_state(self.random_state)
        if self.random_state is not None:
            args['random_state'] = self.random_state

        if self.max_depth != -1:
            args['max_depth'] = self.max_depth

        args['sim_function'] = self.sim_function

        cdef int [:] indicies
        for i in range(self.n_estimators):
            if self.bootstrap == 0:
                self.estimators_.append(CSimilarityTreeCluster(**args).fit(X))
            else:
                indicies = random_state.choice(range(n), n, replace=True).astype(np.int32)
                self.estimators_.append(CSimilarityTreeCluster(**args).fit(X[indicies]))


        return self

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef np.ndarray[np.float32_t, ndim=1] predict_(self, np.ndarray[np.float32_t, ndim=2] X):
        """Produce pairwise distance matrix.
            Parameters
            ----------
            X : array-like matrix of shape = [n_samples, n_features]
                The training data samples.
            Returns
            -------
            distance_matrix : ndarray of shape = comb(n_samples, 2) containing the distances
        """
        cdef int n = X.shape[0]
        cdef np.ndarray[np.float32_t, ndim=1] distance_matrix = np.ones(<int>comb(n, 2), np.float32, order='c')
        cdef float [:] view = distance_matrix

        cdef int num_threads = 4
        cdef int diagonal = 1
        cdef int idx = 0
        cdef float similarity = 0.0
        cdef int i = 0
        cdef int j = 0
        cdef int e = 0
        for i in range(n):
            for j in range(diagonal, n):
                for e in range(self.n_estimators,):
                    similarity += self.estimators_[e].distance(X[i], X[j])

                # similarity is an average depth at which points split across all trees
                #similarity = similarity/<float>self.n_estimators
                # distance = 1 / similarity
                view[idx] = 1 / <float>similarity
                similarity = 0.0
                idx += 1
            diagonal += 1

        return distance_matrix

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef np.ndarray[np.float32_t, ndim=2] ppredict_(self, np.ndarray[np.float32_t, ndim=2] X):
        """Parallel implementation. Produce pairwise distance matrix.
            Parameters
            ----------
            X : array-like matrix of shape = [n_samples, n_features]
                The training data samples.
            Returns
            -------
            distance_matrix : ndarray of shape = [n_samples, n_samples] containing the distances

        Notes
        ------
            In parallel implementation distance is calculated as a sum of 1/similarity across the trees,
            instead of 1 / sum of similarities.
            
            Parallel implementation materializes the whole N*N distance matrix instead of comb(N, 2) flat array.
            Possibly change it in the future.
        """
        cdef int n = X.shape[0]
        cdef float [:, :] X_view = X

        cdef np.ndarray[np.float32_t, ndim=2] distance_matrix = np.zeros(shape=(n, n), dtype=np.float32)
        cdef float [:, :] distance_matrix_view = distance_matrix

        cdef float similarity = 0.0

        cdef int num_threads = 10
        cdef int diagonal = 1
        cdef int i = 0
        cdef int j = 0
        cdef int e = 0
        cdef CSimilarityTreeCluster current_tree

        for e in range(self.n_estimators):
            current_tree = self.estimators_[e]
            for i in range(n):
                for j in prange(n, nogil=True, schedule='dynamic', num_threads=num_threads):
                    if i == j:
                        continue
                    similarity = current_tree.distance(X_view[i], X_view[j])
                    distance_matrix_view[i, j] += <float>similarity#1 / <float>similarity
                    distance_matrix_view[j, i] = distance_matrix_view[i, j]


        return distance_matrix


cdef class CSimilarityTreeCluster:
    """Similarity Tree clusterer."""

    cdef random_state
    cdef str sim_function
    cdef int max_depth
    cdef int depth
    cdef int is_leaf
    cdef float [:] _p
    cdef float [:] _q
    cdef float _split_point
    cdef int [:] lhs_idxs
    cdef int [:] rhs_idxs
    cdef CSimilarityTreeCluster _lhs
    cdef CSimilarityTreeCluster _rhs
    cdef _rng
    cdef f_type projection

    def __cinit__(self,
                  random_state=None,
                  str sim_function='euclidean',
                  int max_depth=-1,
                  int depth=1):
        self.random_state = random_state
        self.sim_function= sim_function
        self.max_depth = max_depth
        self.depth = depth
        self.is_leaf = 0


    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef int is_pure(self, float [:, :] X) nogil:
        """Check if all data-points in the matrix are the same.
            Parameters
            ----------
            X : memoryview of ndarray of shape = [n_samples, n_features]
                The data-points.
            Returns
            -------
            pure : int, 0 indicates that the array is not pure, 1 that it is
        
        """
        cdef int n = X.shape[0]
        cdef int m = X.shape[1]
        cdef int pure = 1
        cdef int i = 0
        cdef int j = 0

        for i in range(n-1):
            for j in range(m):
                # found different row! Not pure
                if X[i, j] != X[i+1, j]:
                    pure = 0
                    break

        return pure

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef int sample_split_direction(self, np.ndarray[np.float32_t, ndim=2] X, int first):
        """Sample index of second data-point to draw split direction. 
            First one was sampled in fit, here we sample only the second one in order to avoid passing a tuple as a result
            Parameters
            ----------
            X : memoryview of ndarray of shape = [n_samples, n_features]
                The data-points.
            first : int, index of first data-point
            Returns
            -------
            second : int, index of second data-point
        
        """
        cdef int n = X.shape[0]
        cdef int m = X.shape[1]
        cdef float [:] first_row = X[first]

        cdef np.ndarray[np.int32_t, ndim=1] others = np.where(np.abs(X - X[first]) > 0)[0].astype(np.int32)
        #assert len(others) > 0, 'All points are the same'
        return self._rng.choice(others, replace=False)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef void _find_split(self, float [:, :] X, f_type projection):
        """Project all data-points, find a split point and indexes of both child partitions.
            Parameters
            ----------
            X : memoryview of ndarray of shape = [n_samples, n_features]
                The data-points.
            projection : f_type, a function used to project data-points
            Returns
            -------
            void
        
        """

        # Calculate similarities
        cdef int n = X.shape[0]
        cdef np.ndarray[np.float32_t, ndim=1] array = np.zeros(n, dtype=np.float32, order='c')
        cdef float [:] similarities = array
        cdef float [:] p = self._p
        cdef float [:] q = self._q

        cdef int num_threads = 4
        if n < 12:
            num_threads = 1
        cdef int i = 0
        # Read about different schedules https://cython.readthedocs.io/en/latest/src/userguide/parallelism.html
        for i in prange(n, schedule='dynamic', nogil=True, num_threads=num_threads):
            similarities[i] = projection(X[i], p, q)

        cdef float similarities_min = np.min(array)
        cdef float similarities_max = np.max(array)

        # Find random split point
        self._split_point = self._rng.uniform(similarities_min, similarities_max, 1)

        # Find indexes of points going left
        self.lhs_idxs = np.nonzero(array <= self._split_point)[0].astype(np.int32)
        self.rhs_idxs = np.nonzero(array > self._split_point)[0].astype(np.int32)


    cpdef CSimilarityTreeCluster fit(self, np.ndarray[np.float32_t, ndim=2] X):
        """Build a tree from the training set X.
            Parameters
            ----------
            X : array-like matrix of shape = [n_samples, n_features]
                The training data samples.
            Returns
            -------
            self : CSimilarityTreeCluster
        """
        cdef int n = X.shape[0]
        if n <= 1:
            self.is_leaf = 1
            return self

        if self.is_pure(X) == 1:
            self.is_leaf = 1
            return self

        if self.max_depth > -1:
            if self.depth == self.max_depth:
                self.is_leaf = 1
                return self

        self._rng = check_random_state(self.random_state)

        cdef int p = 0
        cdef int q = 1
        # if more that two points, find a split
        if n > 2:
            # sample p randomly
            p = self._rng.randint(0, n)

            # sample q so that it's not a copy the same point
            q = self.sample_split_direction(X, p)
            if q == -1:
                raise ValueError(f'Could not find second split point; is_pure should handle that! {np.asarray(X)}')

        self._p = X[p]
        self._q = X[q]

        if self.sim_function == 'dot':
            self.projection = dot_projection
        elif self.sim_function == 'euclidean':
            self.projection = sqeuclidean_projection
        elif self.sim_function == 'rbf':
            self.projection = rbf_projection
        else:
            raise ValueError('Unknown similarity function')

        self._find_split(X, self.projection)

        # if split has been found
        if X[self.lhs_idxs].shape[0] > 0 and X[self.rhs_idxs].shape[0] > 0:
            self._lhs = CSimilarityTreeCluster(random_state=self.random_state,
                                               sim_function=self.sim_function,
                                               max_depth=self.max_depth,
                                               depth=self.depth+1).fit(X[self.lhs_idxs])

            self._rhs = CSimilarityTreeCluster(random_state=self.random_state,
                                               sim_function=self.sim_function,
                                               max_depth=self.max_depth,
                                               depth=self.depth+1).fit(X[self.rhs_idxs])
        else:
            self.is_leaf = 1
            return self

        return self

    cdef int distance(self, float [:] xi, float [:] xj) nogil:
        """Calculate distance of a pair of data-points in tree-space.
            The pair of traverses down the tree, and the depth on which the pair splits is recorded.
            This values serves as a similarity measure between the pair.
            Parameters
            ----------
            X : array-like matrix of shape = [n_samples, n_features]
                The training data samples.
            Returns
            -------
            int : the depth on which the pair splits.
        """
        if self.is_leaf:
            return self.depth

        cdef bint path_i = self.projection(xi, self._p, self._q) <= self._split_point
        cdef bint path_j = self.projection(xj, self._p, self._q) <= self._split_point

        if path_i == path_j:
            # the same path, check if the pair goes left or right
            if path_i:
                return self._lhs.distance(xi, xj)
            else:
                return self._rhs.distance(xi, xj)
        else:
            # different path, return current depth
            return self.depth


    cpdef np.ndarray[np.float32_t, ndim=1] predict_(self, np.ndarray[np.float32_t, ndim=2] X):
        """Produce pairwise distance matrix according to single tree.
            Parameters
            ----------
            X : array-like matrix of shape = [n_samples, n_features]
                The training data samples.
            Returns
            -------
            distance_matrix : ndarray of shape = comb(n_samples, 2) containing the distances
        """
        cdef int n = X.shape[0]
        cdef np.ndarray[np.float32_t, ndim=1] distance_matrix = np.ones(<int>comb(n, 2), dtype=np.float32, order='c')
        cdef float [:] view = distance_matrix

        cdef int diagonal = 1
        cdef int idx = 0
        for c in range(n):
            for r in range(diagonal, n):
                view[idx] = 1 / <float>self.distance(X[c], X[r])
                idx += 1
            diagonal += 1

        return distance_matrix