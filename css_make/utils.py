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


def row_echelon(matrix, full=False):
    """
    Converts a binary matrix to row echelon form via Gaussian Elimination

    Parameters
    ----------
    matrix : numpy.ndarry or scipy.sparse
        A binary matrix in either numpy.ndarray format or scipy.sparse
    full: bool, optional
        If set to `True', Gaussian elimination is only performed on the rows below
        the pivot. If set to `False' Gaussian eliminatin is performed on rows above
        and below the pivot.

    Returns
    -------
        row_ech_form: numpy.ndarray
            The row echelon form of input matrix
        rank: int
            The rank of the matrix
        transform_matrix: numpy.ndarray
            The transformation matrix such that (transform_matrix@matrix)=row_ech_form
        pivot_cols: list
            List of the indices of pivot num_cols found during Gaussian elimination

    Examples
    --------
    >>> H=np.array([[1, 1, 1],[1, 1, 1],[0, 1, 0]])
    >>> re_matrix=row_echelon(H)[0]
    >>> print(re_matrix)
    [[1 1 1]
     [0 1 0]
     [0 0 0]]

    >>> re_matrix=row_echelon(H,full=True)[0]
    >>> print(re_matrix)
    [[1 0 1]
     [0 1 0]
     [0 0 0]]

    """

    num_rows, num_cols = np.shape(matrix)

    the_matrix = to_ndarray_copy(matrix)

    transform_matrix = np.identity(num_rows).astype(int)
    pivot_row = 0
    pivot_cols = []

    # Iterate over cols, for each col find a pivot (if it exists)
    for col in range(num_cols):

        # Select the pivot - if not in this row, swap rows to bring a 1 to this row, if possible
        if the_matrix[pivot_row, col] != 1:

            # Find a row with a 1 in this col
            swap_row_index = pivot_row + np.argmax(the_matrix[pivot_row:num_rows, col])

            # If an appropriate row is found, swap it with the pivot. Otherwise, all zeroes - will loop to next col
            if the_matrix[swap_row_index, col] == 1:
                # Swap rows
                the_matrix[[swap_row_index, pivot_row]] = the_matrix[[pivot_row, swap_row_index]]

                # Transformation matrix update to reflect this row swap
                transform_matrix[[swap_row_index, pivot_row]] = transform_matrix[[pivot_row, swap_row_index]]

        # If we have got a pivot, now let's ensure values below that pivot are zeros
        if the_matrix[pivot_row, col]:

            if not full:
                elimination_range = [k for k in range(pivot_row + 1, num_rows)]
            else:
                elimination_range = [k for k in range(num_rows) if k != pivot_row]

            # Let's zero those values below the pivot by adding our current row to their row
            for j in elimination_range:

                if the_matrix[j, col] != 0 and pivot_row != j:  ### Do we need second condition?

                    the_matrix[j] = the_matrix[j] + the_matrix[pivot_row]
                    the_matrix[j] = the_matrix[j] % 2

                    # Update transformation matrix to reflect this op
                    transform_matrix[j] = (transform_matrix[j] + transform_matrix[pivot_row]) % 2

            pivot_row += 1
            pivot_cols.append(col)

        # Exit loop once there are no more rows to search
        if pivot_row >= num_rows:
            break

    # The rank is equal to the maximum pivot index
    matrix_rank = pivot_row
    row_esch_matrix = the_matrix

    return [row_esch_matrix, matrix_rank, transform_matrix, pivot_cols]
