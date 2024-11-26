import numpy as np
from ldpc.codes import hamming_code

import css_make as cm  # Import the css_make module

H = hamming_code(3)

# Example 1: CssCode类
# The class can be used to create a CSS code from two classical codes.

# 1.1 创建CssCode实例
# 最简创建
qcode1 = cm.CssCode(hx=H)
# -hx参数必须是一个密集矩阵（np.ndarray），或是一个稀疏矩阵（即scipy.sparse.issparse(hx)返回True）
# 如果hx并非上述两种类型，那么将会试图使用np.array(matrix, copy=True)将其转换为密集矩阵
# 如果转换失败，将会抛出TypeError异常

# 完整创建
qcode2 = cm.CssCode(hx=H, hz=H, name="My CSS Code")
# -hz参数如果不提供，则默认为hx（的一个拷贝），输入限制与hx相同
# -name参数如果不提供，则默认为"<Unnamed CSS code>"

# 额外自定义创建参数
qcode3 = cm.CssCode(hx=H, D=np.int64(3))
# 如果提供了完整创建参数以外的参数，那么这些参数将被添加到实例中
# 如果你已经知晓了CssCode的某些参数或是计算结果，并且不期望在CssCode中再次计算它们，那么你可以通过这种方式直接提供这些参数
# 这通常用于避免计算Distance（D）参数，因为计算D参数可能会花费很长时间

# 你也可以通过set方法设置参数，例如如下代码等价于 `qcode4 = cm.CssCode(hx=H, D=np.int64(3))`
qcode4 = cm.CssCode(hx=H)
qcode4.set(D=np.int64(3))

# **但是请注意，如果你提供的自定义参数是由创建参数计算而来的，那么它们将不会被再次验算，因此本包不保证其正确性**

# 1.2 访问CssCode实例的属性
# 你可以直接访问CssCode实例的属性以计算所需的参数或者结果
# 这些属性计算是“惰性”的，即只有在你第一次访问它们时才会进行计算
# 你也可以通过自定义参数创建或是set方法来主动设置这些属性，但是这将导致不再进行主动计算
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

# 1.3 验证CssCode是否有效
# 你可以通过调用test方法来验证CssCode是否有效
qcode = cm.CssCode(hx=H)
qcode.test()
# 该方法会运行一系列测试，以验证CssCode是否有效
# 每一条测试的结果与最终结果都会被打印出来
# 该方法会返回一个布尔值，表示CssCode是否有效

# 你可以通过传递show=False来禁用打印
qcode = cm.CssCode(hx=H)
qcode.test(show=False)

# 一个更便捷的方式是直接调用实例上的valid属性
print(f"qcode is valid: {qcode.valid}")
# 该属性等价于调用test方法并传递show=False
# 该属性也是“惰性”的，即只有在你第一次访问它时才会进行计算
# 你也可以通过自定义参数创建或是set方法来主动设置该属性，但是这将导致不再进行主动计算

# 以上是一个合法CssCode的示例，一下给出一个不能通过验证的示例
from ldpc.codes import rep_code

qcode = cm.CssCode(hx=rep_code(7))
qcode.test()

# Example 2: HGP
# The hypergraph product can be used to construct a valid CSS code from any pair of classical seed codes.
# HGP类的用法与CssCode类类似，但是它一般不接受hx或是hz参数，而是接受h1和h2参数
hgp1 = cm.HGP(h1=H, h2=H, name="My HGP Code")
# 与CssCode完全一致，你可以省略h2参数，此时h2将会被设置为h1（的一个拷贝）
hgp2 = cm.HGP(h1=H)
# 你也可以自定义创建参数
hgp3 = cm.HGP(h1=H, D=np.int64(3))
# HGP实例的属性和方法与CssCode几乎完全一致（只多了`h1`与`h2`属性）
# 你可以通过它们来访问实例的属性和验证实例的有效性
hgp = cm.HGP(h1=H)
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
hgp.test()
print(f"hgp is valid: {hgp.valid}")

# Example 3: 保存
# 你可以通过save方法将CssCode或是HGP实例的属性保存为alist格式的文件
qcode.save(save_property=["hx", "hz"])
# 你需要传递一个属性列表save_property，以及一个可选的code_name参数
# 该方法将会保存属性列表中的每一个属性为一个单独的文件
# 文件名将会以{code_name}_{属性名}.alist的格式保存
# 如果code_name参数未提供，则默认为实例的name属性
