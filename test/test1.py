
import css_make as cm
import numpy as np
import scipy

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

result = cm.cm_mod2.row_echelon(H)
print(result[3])

H_sparse = scipy.sparse.csr_matrix(H)
result = cm.cm_mod2.row_echelon(H_sparse)
print(result[3])

H_csc = scipy.sparse.csc_matrix(H)
result = cm.cm_mod2.row_echelon(H_csc)
print(result[3])

from ldpc.codes import hamming_code

H = hamming_code(3).toarray()
qcode = cm.CssCode(hx=H, hz=H)
print(qcode.code_params)

print(qcode.lx)
print(qcode.lz)

qcode.test()
