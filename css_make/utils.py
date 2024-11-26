import numpy as np
from scipy.sparse import issparse


def to_ndarray_copy(matrix):
    """
    Check if the input is a dense numpy array or a sparse matrix and convert it to a dense numpy array.

    Args:
        matrix: The input to be checked or converted.

    Returns:
        np.ndarray: A dense numpy array (copy).

    Raises:
        TypeError: If the input is not a dense numpy array or a sparse matrix, and cannot be converted.
    """
    if isinstance(matrix, np.ndarray):
        return np.copy(matrix)

    if issparse(matrix):
        return matrix.toarray()

    try:
        print("Trying to convert the input to a dense numpy array")
        return np.array(matrix, copy=True)
    except Exception as e:
        raise TypeError("Input is not a dense numpy array and cannot be converted.") from e
