# css_make

## Overview

`css_make` is a Python library implementing belief propagation with ordered statistics post-processing for decoding
sparse quantum LDPC codes as described in [arXiv:2005.07016](https://arxiv.org/abs/2005.07016).

`css_make` is the successor to `bp_osd` (a component of the `ldpc` package).

Since the `bp_osd` project is no longer maintained and cannot run on currently supported Python versions, this package
aims to serve as a replacement and an upgrade for `bp_osd`.

Additionally, this package has significantly refactored `bp_osd` to address bugs, improve readability and extensibility,
and enhance robustness.

However, note that the interfaces of this package differ from those of `bp_osd`. Please refer to the documentation when
using it.

## Features

`css_make` provides a powerful set of tools for constructing and verifying sparse quantum LDPC codes, supporting the
following key features:

1. **Constructing CSS codes**:
    - Offers the `CssCode` class to construct CSS codes from classical codes.
    - Enables efficient access to properties such as distance (`D`), code length (`N`), and logical qubit count (`K`)
      through lazy evaluation.
    - Supports automated testing and verification via the `test()` method or the `valid` attribute, making it easy to
      check the validity of CSS codes.

2. **Hypergraph product codes**:
    - Provides the `HGP` class for generating CSS codes from classical seed codes with flexible parameter settings.
    - Maintains an interface consistent with the `CssCode` class, making it easy to learn and use.

3. **Custom parameter support**:
    - Allows additional parameters to be passed during instance creation to avoid redundant computations and improve
      efficiency.
    - Custom parameters are directly added as attributes of the instance.

4. **File saving functionality**:
    - Includes a `save` method for saving the matrix properties of CSS or HGP codes in `.alist` format, facilitating
      integration with other toolchains.

5. **Improved user experience**:
    - Fixes several known issues in the original `bp_osd` package and improves code readability and robustness.
    - Provides detailed documentation and example code to help users get started quickly.

## Installation

Install the package using pip:

```bash
pip install css_make
```

## TODO

The BP+OSD Decoding functionality in `bp_osd` has not yet been implemented.

## How to Use

### Prerequisites

```python
import numpy as np
from ldpc.codes import hamming_code
import css_make as cm  # Import the css_make package

H = hamming_code(3)
```

For demonstration purposes, we use the `hamming_code` function from the `ldpc.codes` package to generate a Hamming code
as an example.

### Example 1: `CssCode` Class

The class can be used to create a CSS code from two classical codes.

#### 1.1 Creating a `CssCode` Instance

##### Minimal Creation

You can create the simplest `CssCode` instance by providing only the `hx` parameter:

```python
qcode = cm.CssCode(hx=H)
```

- The `hx` parameter must be a dense matrix (`np.ndarray`) or a sparse matrix (i.e., `scipy.sparse.issparse(hx)` returns
  `True`).
- If `hx` is not one of the above types, the program will attempt to convert it into a dense matrix using
  `np.array(matrix, copy=True)`. If the conversion fails, a `TypeError` will be raised.

##### Full Creation

You can provide both the `hx` and `hz` parameters, along with optional `name` and `compute_distance_timeout` parameters, for full creation:

```python
qcode = cm.CssCode(hx=H, hz=H, name="My CSS Code", compute_distance_timeout=2.0)
```

- If the `hz` parameter is not provided, it defaults to a copy of `hx`.
- The `name` parameter defaults to `"<Unnamed CSS code>"` if not provided.
- When calculating the code distance, if the input matrix has more than 15 columns, the system will automatically invoke `ldpc.code_util.estimate_code_distance`. In this case, the `compute_distance_timeout` parameter will be passed as the `timeout_seconds` argument to this function, defaulting to 1.0 seconds.

##### Using Additional Custom Parameters

You can also pass additional parameters during instance creation, such as:

```python
qcode = cm.CssCode(hx=H, D=np.int64(3))
```

- Custom parameters will be directly added to the instance.
- This is often used to avoid recalculating certain attributes (like distance `D`) when such calculations are
  time-consuming.

##### Setting Parameters with the `set` Method

In addition to providing parameters during creation, you can dynamically set attributes using the `set` method:

```python
qcode = cm.CssCode(hx=H)
qcode.set(D=np.int64(3))
```

**Note: If an attribute is derived from additional custom parameters or overwritten using the `set` method, it will not
be recalculated. The correctness of such attributes is the user's responsibility.**

#### 1.2 Accessing `CssCode` Instance Attributes

Once an instance is created, you can directly access its attributes to retrieve parameters or results. These attributes
are lazily evaluated, meaning they are only calculated when accessed for the first time:

```python
qcode = cm.CssCode(hx=H)
print(f"qcode: {qcode}")
print(f"N: {qcode.N}")
print(f"K: {qcode.K}")
print(f"L: {qcode.L}")
print(f"Q: {qcode.Q}")
print(f"h: {qcode.h}")
print(f"lx: {qcode.lx}")
print(f"lz: {qcode.lz}")
print(f"l: {qcode.l}")
print(f"canonical_lx: {qcode.canonical_lx}")
print(f"canonical_lz: {qcode.canonical_lz}")
print(f"D: {qcode.D}")
print(f"code_params: {qcode.code_params}")
```

#### 1.3 Verifying the Validity of a `CssCode`

You can verify the validity of a `CssCode` by calling the `test` method:

```python
qcode = cm.CssCode(hx=H)
qcode.test()
```

- This method runs a series of tests to check the validity of the `CssCode`. Test results are printed to the console,
  and a boolean value is returned.
- You can suppress console output by passing `show=False`:
  ```python
  qcode.test(show=False)
  ```

Alternatively, you can directly access the `valid` attribute for a more convenient check:

```python
print(f"qcode is valid: {qcode.valid}")
```

- This attribute is equivalent to calling `test(show=False)` and is also lazily evaluated.

Here is an example of an invalid code that fails validation:

```python
from ldpc.codes import rep_code

qcode = cm.CssCode(hx=rep_code(7))
qcode.test()
```

### Example 2: `HGP` Class

The hypergraph product can be used to construct a valid CSS code from any pair of classical seed codes.

This class behaves almost identically to the `CssCode` class. The following outlines the differences.

#### 2.1 Creating an `HGP` Instance

Use the `HGP` class to generate a CSS code:

```python
hgp = cm.HGP(h1=H, h2=H, name="My HGP Code")
```

- The `h2` parameter can be omitted, in which case it defaults to a copy of `h1`.
- Custom parameters are also supported, such as:
  ```python
  hgp = cm.HGP(h1=H, D=np.int64(3))
  ```

#### 2.2 Accessing `HGP` Instance Attributes

The `HGP` class has attributes and methods nearly identical to those of the `CssCode` class, with the addition of `h1`
and `h2` attributes:

```python
print(f"hgp: {hgp}")
print(f"N: {hgp.N}")
print(f"K: {hgp.K}")
print(f"L: {hgp.L}")
print(f"Q: {hgp.Q}")
print(f"h: {hgp.h}")
print(f"lx: {hgp.lx}")
print(f"lz: {hgp.lz}")
print(f"l: {hgp.l}")
print(f"canonical_lx: {hgp.canonical_lx}")
print(f"canonical_lz: {hgp.canonical_lz}")
print(f"D: {hgp.D}")
print(f"code_params: {hgp.code_params}")
```

#### 2.3 Verifying the Validity of an `HGP`

You can verify the validity of an `HGP` instance using the `test` method or the `valid` attribute:

```python
hgp.test()
print(f"hgp is valid: {hgp.valid}")
```

### Example 3: Saving

You can use the `save` method to save the properties of a `CssCode` or `HGP` instance in `.alist` format:

```python
qcode.save(save_property=["hx", "hz"], code_name="example_code")
```

- The `save_property` parameter is a list of attribute names specifying which properties to save.
- The `code_name` parameter customizes the filename prefix. If not provided, it defaults to the instance's `name`
  attribute.

The files are saved with the format `{code_name}_{attribute_name}.alist`.

## Contributing

Feel free to open issues or submit pull requests if you encounter bugs or have feature requests.

## Acknowledgments

This project is modified from the following two projects, and includes selected files or components under the MIT
License:

1. **bp_osd** ([GitHub Repository](https://github.com/quantumgizmos/bp_osd))
2. ~~**ldpc** ([GitHub Repository](https://github.com/quantumgizmos/ldpc))~~

The included files have been modified to fit the specific needs of this project. For details about the modifications,
see the respective directories under `third_party/`. The original LICENSE files from these projects are preserved.
