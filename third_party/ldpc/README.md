# ldpc (Modified)

This directory contains files modified from the project **ldpc** ([GitHub Repository](https://github.com/quantumgizmos/ldpc)), which is licensed under the MIT License.

## Included Files
The following file from the original `ldpc` project has been referenced and modified:
- `/src_python/ldpc/mod2/mod2_numpy.py`

## Modifications
1. **Extracted `row_echelon` Function**:
   - The `row_echelon` function from the original implementation has been extracted for standalone use and further extended.

2. **Added Support for CSC Matrices**:
   - Enhanced the `row_echelon` function to include compatibility with Compressed Sparse Column (CSC) matrices.
   - This improvement broadens the function's applicability to sparse matrix operations, ensuring better performance and memory efficiency for large-scale matrices.

## License
This modified version retains the original license of the `ldpc` project. For details, refer to the `LICENSE` file in this directory.

## Acknowledgments
Special thanks to the original authors of the `ldpc` project for their foundational work, which has been adapted and improved upon in this project.
