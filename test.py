# `css_make` is a package designed as a patching solution to address specific issues in existing tools, particularly the `mod2.row_echelon` function in the `ldpc` package and the `css_code` class in the bp_osd package.
# In the `ldpc` package, the `mod2.row_echelon` function struggled to correctly process certain matrix formats, leading to errors when handling sparse matrices.
# Meanwhile, the `css_code` class in `bp_osd` exhibited unexpected behavior due to implementation bugs, hindering its intended functionality.
# This package provides targeted fixes for these problems while maintaining compatibility with the original workflows.
# PS: If you've encountered errors like `ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all().` while using these functionalities in the original packages, don’t hesitate——this project is likely the solution you need!

# Using the css_make module
import css_make as cm  # Import the css_make module
import numpy as np
import scipy

# Create a dense matrix (Dense Matrix)
H = np.array([[1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
              [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
              [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
              [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
              [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
              [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]])

# Example 1: Using mod2_numpy.row_echelon
# cm.mod2_numpy.row_echelon produces results equivalent to ldpc.mod2.row_echelon.
# In addition, this function **correctly** supports dense matrices (ndarray),
# CSR-format sparse matrices, and CSC-format sparse matrices.
# For other formats, the function attempts to convert them to ndarray format.
# Note: If the conversion fails, the function will print an error message and return None.

# 1.1 Processing a dense matrix
result = cm.cm_mod2.row_echelon(H)
assert result is not None  # If the return value is None, it might be due to the input matrix not being converted to ndarray format. Check the error message for details.
print("Dense Matrix (ndarray) Row Echelon:")
print(result[3])

# 1.2 Processing a CSR-format sparse matrix
H_sparse = scipy.sparse.csr_matrix(H)
result = cm.cm_mod2.row_echelon(H_sparse)
assert result is not None
print("CSR Sparse Matrix Row Echelon:")
print(result[3])

# 1.3 Processing a CSC-format sparse matrix
H_csc = scipy.sparse.csc_matrix(H)
result = cm.cm_mod2.row_echelon(H_csc)
assert result is not None
print("CSC Sparse Matrix Row Echelon:")
print(result[3])

# Example 2: Using the CssCode class
# The CssCode class provides functionality similar to bposd.css.css_code
# but resolves issues in the original implementation.
from ldpc.codes import hamming_code

H = hamming_code(3).toarray()  # Generate a Hamming code matrix
qcode = cm.CssCode(hx=H, hz=H)  # Create a CssCode instance

# Inspect the logical operations of CssCode
print("CssCode Logical X:")
print(qcode.lx.toarray())  # Print the logical X operation result
print("CssCode Logical Z:")
print(qcode.lz.toarray())  # Print the logical Z operation result

# Example 3: Using the stab.StabCode class
# The StabCode class is equivalent to the stab_code in /src/bposd/stab.py,
# and serves as a dependency for other modules in this context.
print("StabCode is available as a dependency.")
