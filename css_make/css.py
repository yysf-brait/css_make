import numpy as np
from ldpc import mod2
from ldpc.alist import save_alist
from ldpc.code_util import compute_code_distance

from . import stab


class CssCode:
    tests_list = [
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
    def compute_lz(hx, hz):
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
                 hx: np.array = None,
                 hz: np.array = None,
                 code_distance=0,
                 name: str = "<Unnamed CSS code>"):

        self.hx = hx if hx is not None else np.array([[]])  # hx pcm
        self.hz = hz if hz is not None else np.array([[]])  # hz pcm
        self.D = code_distance  # code distance
        self.name = name

        if self.N == 0:
            print("Warning: hx and hz matrices are both have 0 columns!")
            return

        if self.D != 0:
            print("Info: code distance is not 0, Skipping code distance calculation")
            return

        dx = compute_code_distance(hx)
        dz = compute_code_distance(hz)
        self.D = np.min([dx, dz])

    def __str__(self) -> str:
        return f"{self.name} <params: {self.code_params}>"

    @property
    def N(self):  # noqa
        """Block Length"""
        if self.hx.shape[1] != self.hz.shape[1]:
            raise Exception("Error: hx and hz matrices must have equal numbers of columns!")
        return self.hx.shape[1]

    @property
    def K(self):  # noqa
        """Code Dimension"""
        return self.N - mod2.rank(self.hx) - mod2.rank(self.hz)

    @property
    def L(self):  # noqa
        """LDPC params - max column weight"""
        hx_l = np.max(np.sum(self.hx, axis=0))
        hz_l = np.max(np.sum(self.hz, axis=0))
        return np.max([hx_l, hz_l]).astype(int)

    @property
    def Q(self):  # noqa
        """LDPC params - max row weight"""
        hx_q = np.max(np.sum(self.hx, axis=1))
        hz_q = np.max(np.sum(self.hz, axis=1))
        return np.max([hx_q, hz_q]).astype(int)

    @property
    def h(self):
        hx = np.vstack([np.zeros(self.hz.shape, dtype=int), self.hx])
        hz = np.vstack([self.hz, np.zeros(self.hx.shape, dtype=int)])
        return np.hstack([hx, hz])

    @property
    def lx(self):
        """x logicals"""
        return self.compute_lz(self.hz, self.hx)

    @property
    def lz(self):
        """z logicals"""
        return self.compute_lz(self.hx, self.hz)

    @property
    def l(self):
        lx = np.vstack([np.zeros(self.lz.shape, dtype=int), self.lx])
        lz = np.vstack([self.lz, np.zeros(self.lx.shape, dtype=int)])
        return np.hstack([lx, lz])

    @property
    def code_params(self):
        return f"({self.L},{self.Q})-[[{self.N},{self.K},{self.D}]]"

    def save_sparse(self, code_name: str | None = None):
        """
        Save the code in alist format
        If code_name is not provided, the code name is used
        """
        if code_name is None:
            code_name = self.name

        save_alist(f"{code_name}_hx.alist", self.hx)
        save_alist(f"{code_name}_hz.alist", self.hz)
        save_alist(f"{code_name}_lx.alist", self.lx)
        save_alist(f"{code_name}_lz.alist", self.lz)

    # 该函数会修改D，不清楚目的，暂时保留
    def compute_code_distance(self):
        def to_stab_code():
            hx = np.vstack([np.zeros(self.hz.shape, dtype=int), self.hx])
            hz = np.vstack([self.hz, np.zeros(self.hx.shape, dtype=int)])
            return stab.StabCode(hx, hz)

        temp = to_stab_code()
        self.D = temp.compute_code_distance()
        return self.D

    # 该函数会修改lx，不清楚目的，暂时保留
    def canonical_logicals(self):
        temp = mod2.inverse(self.lx @ self.lz.T % 2)
        self.lx = temp @ self.lx % 2

    def test(self, show: bool = True) -> bool:
        results = {}

        print(f"Testing {str(self)} ..")
        for name, condition in self.tests_list:
            try:
                results[name] = condition(self)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Failed test: {name}, the property used in the test might be incorrect")
                results[name] = None

        valid = all(results.values())
        if not show:
            return valid

        print("Test result:")
        for name, condition in results.items():
            if condition is None:
                print(f"\033[31m{name}: Skipped\033[0m")
            if condition is False:
                print(f"\033[31m{name}: Failed\033[0m")
            if condition is True:
                print(f"\033[32m{name}: Passed\033[0m")

        if valid:
            print(f"{str(self)} is a valid CSS code")
        else:
            print(f"\033[31m{str(self)} is an **invalid** CSS code\033[0m")

        return valid
