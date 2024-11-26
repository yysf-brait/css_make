import traceback
from functools import cached_property
from typing import List

import numpy as np
from ldpc import mod2
from ldpc.alist import save_alist
from ldpc.code_util import compute_code_distance

from . import utils


class CssCode:
    _tests_list = [
        ("Block dimensions[N, K, lz, lx]",
         lambda self: self.N == self.lz.shape[1] == self.lx.shape[1] and self.K == self.lz.shape[0] == self.lx.shape[
             0]),
        ("PCMs commute hz@hx.T==0[hz, hx]",
         lambda self: not (self.hz @ self.hx.T % 2).any()),
        ("PCMs commute hx@hz.T==0[hx, hz]",
         lambda self: not (self.hx @ self.hz.T % 2).any()),
        ("-lx \in ker{hz} AND lz \in ker{hx}[hz, lx]",
         lambda self: not (self.hz @ self.lx.T % 2).any()),
        ("-lx \in ker{hz} AND lz \in ker{hx}[hx, lz]",
         lambda self: not (self.hx @ self.lz.T % 2).any()),
        ("-lx and lz anticommute[lx, lz]",
         lambda self: mod2.rank(self.lx @ self.lz.T % 2) == self.K)
    ]

    @staticmethod
    def _compute_lz(hx, hz):
        # lz logical operators
        # lz\in ker{hx} AND \notin Im(Hz.T)

        ker_hx = mod2.nullspace(hx).toarray()  # compute the kernel basis of hx
        im_hzT = mod2.row_basis(hz).toarray()  # compute the image basis of hz.T # noqa

        # in the below we row reduce to find vectors in kx that are not in the image of hz.T.
        log_stack = np.vstack([im_hzT, ker_hx])
        pivots = mod2.row_echelon(log_stack.T)[3]
        log_op_indices = [i for i in range(im_hzT.shape[0], log_stack.shape[0]) if i in pivots]
        log_ops = log_stack[log_op_indices]

        return log_ops

    def __init__(self,
                 hx=None,
                 hz=None,
                 name: str = "<Unnamed CSS code>",
                 **kwargs):

        self.hx = utils.to_ndarray_copy(hx) if hx is not None else np.array([[]])  # hx pcm
        self.hz = utils.to_ndarray_copy(hz) if hz is not None else np.copy(self.hx)  # hz pcm
        self.name = name

        if self.N == 0:
            print("Warning: hx and hz matrices are both have 0 columns. So the N is 0!")
            return

        self.set(**kwargs)

    def __str__(self) -> str:
        return f"{self.name} <params: {self.code_params}>"

    def set(self, **kwargs) -> None:
        """
        Update the code parameters
        If a cached property is overwritten, a warning is printed.
        """
        for key, value in kwargs.items():
            if hasattr(self.__class__, key) and isinstance(getattr(self.__class__, key), cached_property):
                print(f"Warning: '{key}' is a cached property. Overwriting it may lead to inconsistent behavior.")
            setattr(self, key, value)

    @cached_property
    def N(self):  # noqa
        """Block Length"""
        if self.hx.shape[1] != self.hz.shape[1]:
            raise Exception("Error: hx and hz matrices must have equal numbers of columns!")
        return self.hx.shape[1]

    @cached_property
    def K(self):  # noqa
        """Code Dimension"""
        return self.N - mod2.rank(self.hx) - mod2.rank(self.hz)

    @cached_property
    def L(self):  # noqa
        """LDPC params - max column weight"""
        hx_l = np.max(np.sum(self.hx, axis=0))
        hz_l = np.max(np.sum(self.hz, axis=0))
        return np.max([hx_l, hz_l]).astype(int)

    @cached_property
    def Q(self):  # noqa
        """LDPC params - max row weight"""
        hx_q = np.max(np.sum(self.hx, axis=1))
        hz_q = np.max(np.sum(self.hz, axis=1))
        return np.max([hx_q, hz_q]).astype(int)

    @cached_property
    def h(self):
        hx = np.vstack([np.zeros(self.hz.shape, dtype=int), self.hx])
        hz = np.vstack([self.hz, np.zeros(self.hx.shape, dtype=int)])
        return np.hstack([hx, hz])

    @cached_property
    def lx(self):
        """x logicals"""
        return self._compute_lz(self.hz, self.hx)

    @cached_property
    def lz(self):
        """z logicals"""
        return self._compute_lz(self.hx, self.hz)

    @cached_property
    def l(self):
        lx = np.vstack([np.zeros(self.lz.shape, dtype=int), self.lx])
        lz = np.vstack([self.lz, np.zeros(self.lx.shape, dtype=int)])
        return np.hstack([lx, lz])

    @cached_property
    def canonical_lx(self):
        """Return the canonical logicals for the X stabilizers"""
        temp = mod2.inverse(self.lx @ self.lz.T % 2)
        return temp @ self.lx % 2

    @cached_property
    def canonical_lz(self):
        """Return the canonical logicals for the Z stabilizers"""
        return self.lz

    @cached_property
    def D(self):  # noqa
        dx = compute_code_distance(self.hx)
        dz = compute_code_distance(self.hz)
        return np.min([dx, dz])

    @cached_property
    def valid(self):
        return self.test(show=False)

    @cached_property
    def code_params(self):
        return f"({self.L},{self.Q})-[[{self.N},{self.K},{self.D}]]"

    def save(self, save_property: List[str], code_name: str | None = None):
        """
        Save the code in alist format
        save_property: List of properties to save
        code_name: Name of the code
        """
        if code_name is None:
            code_name = self.name
        for prop in save_property:
            if not hasattr(self, prop) or not isinstance(getattr(self, prop), np.ndarray):
                print(f"Property '{prop}' is not a valid numpy array. Skipping ..")
            save_alist(f"{code_name}_{prop}.alist", getattr(self, prop))

    def test(self, show: bool = True) -> bool:
        results = {}

        if show:
            print(f"Testing {str(self)} ..")
        for name, condition in self._tests_list:
            try:
                results[name] = condition(self)
            except Exception as e:
                print(f"Error while testing '{name}': {e}")
                traceback.print_exc()
                print(f"Failed test: {name}, the property used in the test might be incorrect")
                results[name] = None

        valid = all(results.values())
        if not show:
            return valid

        print("Test logs:")
        for name, condition in results.items():
            if condition is None:
                print(f"\033[31m{name}: Skipped\033[0m")
            if condition is False:
                print(f"\033[31m{name}: Failed\033[0m")
            if condition is True:
                print(f"\033[32m{name}: Passed\033[0m")

        print("Final result:")
        if valid:
            print(f"\033[32m{str(self)} is a valid CSS code\033[0m")
        else:
            print(f"\033[31m{str(self)} is an **invalid** CSS code\033[0m")

        return valid


class HGP(CssCode):
    def __init__(self,
                 h1=None,
                 h2=None,
                 name: str = "<Unnamed HGP>",
                 **kwargs):
        self.h1 = utils.to_ndarray_copy(h1) if h1 is not None else np.array([[]])
        self.h2 = utils.to_ndarray_copy(h2) if h2 is not None else np.copy(self.h1)

        m1, n1 = np.shape(self.h1)
        m2, n2 = np.shape(self.h2)

        i_m1, i_n1 = np.eye(m1, dtype=int), np.eye(n1, dtype=int)
        i_m2, i_n2 = np.eye(m2, dtype=int), np.eye(n2, dtype=int)

        # construct hx and hz
        hx = np.hstack([
            np.kron(self.h1, i_n2),  # hx1
            np.kron(i_m1, self.h2.T)  # hx2
        ])

        hz = np.hstack([
            np.kron(i_n1, self.h2),  # hz1
            np.kron(self.h1.T, i_m2)  # hz2
        ])

        super().__init__(hx=hx, hz=hz, name=name, **kwargs)

    @cached_property
    def D(self):
        d1 = compute_code_distance(self.h1)
        d1t = compute_code_distance(self.h1.T)
        d2 = compute_code_distance(self.h2)
        d2t = compute_code_distance(self.h2.T)
        return np.min([d1, d1t, d2, d2t]).astype(int)
