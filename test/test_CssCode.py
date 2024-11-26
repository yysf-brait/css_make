from ldpc.codes import hamming_code

import css_make as cm

H = hamming_code(3)
qcode = cm.CssCode(hx=H, hz=H)

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
qcode.test()
