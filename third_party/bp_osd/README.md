# bp_osd (Modified)

This directory contains files modified from the project **bp_osd
** ([GitHub Repository](https://github.com/quantumgizmos/bp_osd)), which is licensed under the MIT License.

## Included Files

The following files from the original `bp_osd` project have been referenced and modified:

- `/src/bposd/css.py`
- ~~`/src/bposd/stab.py`~~

## Modifications

1. ~~**Replaced `row_echelon` Function**~~:
    - The original `row_echelon` function has been replaced with a custom implementation to fix an identified bug in the
      original version.
    - The new implementation improves accuracy and reliability, ensuring proper functionality under edge cases.

2. **Code Optimization**:
    - Improved naming conventions to make the codebase more readable and aligned with standard Python practices (PEP 8).
    - Refined parts of the syntax, enhancing code clarity and maintainability.

3. **Rewritten**:
    - With `css_make` version > 1.1.0, only the core calculation logic has been retained, and the code has been
      significantly refactored.

## License

This modified version retains the original license of the `bp_osd` project. For details, refer to the `LICENSE` file in
this directory.

## Acknowledgments

Special thanks to the original authors of the `bp_osd` project for their foundational work, which has been adapted and
improved upon in this project.
