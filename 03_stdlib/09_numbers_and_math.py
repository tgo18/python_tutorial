"""
Python3 数字与数学 —— 写给 Java 开发者

核心概念：
- Python 的 int 没有溢出问题（无限精度），这点比 Java 强大得多
- 类比 Java: decimal.Decimal ≈ BigDecimal，math ≈ Math
- 金融计算务必用 Decimal，不要用 float
"""

import math
import decimal
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from fractions import Fraction
import random


# =============================================================================
# 1. Python 内置数字类型
# =============================================================================

def builtin_number_types():
    """Python 内置数字类型 vs Java 数字类型"""

    print("=" * 60)
    print("1. Python 内置数字类型")
    print("=" * 60)

    # --- int: 无限精度整数 ---
    # Java: int(32位)/long(64位) 会溢出，大数需要 BigInteger
    # Python: int 天然无限精度，永不溢出！
    print(f"小整数: 42, type: {type(42).__name__}")
    print(f"2^100 = {2 ** 100}")                            # Java int/long 早就溢出了
    print(f"10^1000 有 {len(str(10 ** 1000))} 位数")         # Python 毫无压力
    print(f"100! 有 {len(str(math.factorial(100)))} 位数")   # Java 需要 BigInteger

    # --- float: 64位双精度浮点（等价于 Java double） ---
    print(f"\nfloat: {3.14}, 科学计数法: {2.5e10}")
    print(f"inf: {float('inf')}, nan: {float('nan')}")
    print(f"nan == nan: {float('nan') == float('nan')}")   # False! NaN 不等于自身
    print(f"浮点陷阱: 0.1 + 0.2 = {0.1 + 0.2}")           # 0.30000000000000004

    # --- complex: 复数（Java 无原生支持） ---
    c = 3 + 4j                              # j 是虚数单位（数学中的 i）
    print(f"\n复数: {c}, 实部: {c.real}, 虚部: {c.imag}, 模: {abs(c)}")

    # --- bool 是 int 的子类（Java 中 boolean 和 int 完全独立） ---
    print(f"\nTrue + True = {True + True}")   # 2（Java 中编译错误）
    print(f"isinstance(True, int): {isinstance(True, int)}")


# =============================================================================
# 2. 算术运算符
# =============================================================================

def arithmetic_operators():
    """算术运算符 vs Java"""

    print("\n" + "=" * 60)
    print("2. 算术运算符")
    print("=" * 60)

    print("基本: 10+3={}, 10-3={}, 10*3={}".format(10+3, 10-3, 10*3))

    # 除法: Python vs Java 最大的坑
    # Java: 10 / 3 = 3（截断小数）  Python: 10 / 3 = 3.333...（真除法）
    print(f"\n除法（注意与 Java 的区别）:")
    print(f"  10 / 3  = {10 / 3}")          # 3.333... 真除法，永远返回 float
    print(f"  10 // 3 = {10 // 3}")         # 3  整除（等价于 Java 的 10/3）
    print(f"  10 % 3  = {10 % 3}")          # 1  取模

    # 负数取整方向不同！Java 向零截断，Python 向下取整
    print(f"\n负数除法（又一个坑）:")
    print(f"  Python: -7 // 2 = {-7 // 2}, -7 % 2 = {-7 % 2}")    # -4, 1
    print(f"  Java:   -7 / 2  = -3,         -7 % 2 = -1（向零截断）")

    # 幂运算: Java 用 Math.pow() 返回 double，Python 用 ** 运算符
    print(f"\n幂运算:")
    print(f"  2 ** 10  = {2 ** 10}")            # 1024（int）
    print(f"  2 ** 0.5 = {2 ** 0.5}")           # 1.414...（float）
    print(f"  pow(2, 10, 1000) = {pow(2, 10, 1000)}")  # 24，快速模幂

    # divmod: 同时获取商和余数（Java 无对应）
    q, r = divmod(17, 5)
    print(f"\ndivmod(17, 5) = 商 {q}, 余 {r}")

    # round() 使用银行家舍入（四舍六入五取偶）
    print(f"\nround(2.5) = {round(2.5)}")       # 2（不是 3！）
    print(f"round(3.5) = {round(3.5)}")         # 4
    print(f"round(3.14159, 2) = {round(3.14159, 2)}")


# =============================================================================
# 3. math 模块
# =============================================================================

def math_module_demo():
    """math 模块 vs Java Math 类"""

    print("\n" + "=" * 60)
    print("3. math 模块")
    print("=" * 60)

    # 常量（Java: Math.PI, Math.E）
    print(f"math.pi={math.pi}, math.e={math.e}")
    print(f"math.inf={math.inf}, math.nan={math.nan}")

    # 取整（Python 返回 int，Java Math.ceil/floor 返回 double）
    print(f"\n取整:")
    print(f"  ceil(3.2)={math.ceil(3.2)}, ceil(-3.2)={math.ceil(-3.2)}")
    print(f"  floor(3.8)={math.floor(3.8)}, floor(-3.8)={math.floor(-3.8)}")
    print(f"  trunc(3.8)={math.trunc(3.8)}, trunc(-3.8)={math.trunc(-3.8)}")

    # 常用函数
    print(f"\n常用函数:")
    print(f"  sqrt(16)={math.sqrt(16)}, log(e)={math.log(math.e)}")
    print(f"  log10(100)={math.log10(100)}, log2(1024)={math.log2(1024)}")
    print(f"  pow(2,10)={math.pow(2, 10)}")   # 返回 float，区别于内置 **

    # 三角函数（弧度制）
    print(f"\n三角函数:")
    print(f"  sin(π/2)={math.sin(math.pi/2)}, cos(0)={math.cos(0)}")
    print(f"  degrees(π)={math.degrees(math.pi)}, radians(180)={math.radians(180):.4f}")

    # 实用工具
    print(f"\n实用工具:")
    print(f"  gcd(12,8)={math.gcd(12, 8)}, factorial(10)={math.factorial(10)}")
    print(f"  isclose(0.1+0.2, 0.3) = {math.isclose(0.1 + 0.2, 0.3)}")  # True!
    print(f"  isinf(inf)={math.isinf(math.inf)}, isnan(nan)={math.isnan(math.nan)}")


# =============================================================================
# 4. decimal 模块 —— 精确十进制计算
# =============================================================================

def decimal_module_demo():
    """decimal.Decimal vs Java BigDecimal"""

    print("\n" + "=" * 60)
    print("4. decimal 模块（金融计算必备）")
    print("=" * 60)

    # Java: BigDecimal price = new BigDecimal("19.99");
    # Python: price = Decimal("19.99")
    # 核心规则：用字符串创建 Decimal，不要用 float!
    print("float vs Decimal:")
    print(f"  float:   0.1 + 0.2 = {0.1 + 0.2}")
    print(f"  Decimal: 0.1 + 0.2 = {Decimal('0.1') + Decimal('0.2')}")

    # 千万不要用 float 创建 Decimal！
    bad = Decimal(0.1)       # 精度已丢失
    good = Decimal('0.1')    # 精确
    print(f"\n  Decimal(0.1)   = {bad}")       # 0.10000000000000000555...
    print(f"  Decimal('0.1') = {good}")         # 0.1

    # 商品计算示例
    price, tax_rate = Decimal('19.99'), Decimal('0.08')
    subtotal = price * 3
    tax = subtotal * tax_rate
    print(f"\n商品计算: 单价={price} x 3 = {subtotal}, 税={tax}")

    # 精度控制（Java: setScale(2, RoundingMode.HALF_UP)）
    rounded = tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    print(f"  税额四舍五入到分: {rounded}")

    # 全局/局部精度
    print(f"\n精度控制 (当前={decimal.getcontext().prec}位):")
    print(f"  1/3 = {Decimal(1) / Decimal(3)}")
    with decimal.localcontext() as ctx:
        ctx.prec = 50
        print(f"  50位: 1/3 = {Decimal(1) / Decimal(3)}")

    # 舍入模式（Java 对应 RoundingMode）
    val = Decimal('2.5')
    print(f"\n舍入模式:")
    print(f"  ROUND_HALF_UP:   2.5 -> {val.quantize(Decimal('1'), rounding=ROUND_HALF_UP)}")
    print(f"  ROUND_HALF_EVEN: 2.5 -> {val.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)}")


# =============================================================================
# 5. fractions 模块 —— 分数运算
# =============================================================================

def fractions_demo():
    """分数运算 —— Java 无原生支持"""

    print("\n" + "=" * 60)
    print("5. fractions 模块")
    print("=" * 60)

    # Java 需要自己写分数类或用第三方库，Python 内置
    f1 = Fraction(1, 3)         # 1/3
    f2 = Fraction(2, 5)         # 2/5
    print(f"创建: 1/3={f1}, 2/5={f2}, 从字符串={Fraction('3.14')}, 从float={Fraction(0.5)}")

    # 分数运算（自动约分）
    print(f"\n运算:")
    print(f"  1/3 + 2/5 = {f1 + f2}")       # 11/15
    print(f"  1/3 * 2/5 = {f1 * f2}")       # 2/15
    print(f"  1/3 / 2/5 = {f1 / f2}")       # 5/6

    # 分数近似
    print(f"\n最佳分数近似:")
    print(f"  0.1 ≈ {Fraction(0.1).limit_denominator(10)}")
    print(f"  π   ≈ {Fraction(math.pi).limit_denominator(1000)}")   # 355/113


# =============================================================================
# 6. 进制转换
# =============================================================================

def base_conversion_demo():
    """进制转换"""

    print("\n" + "=" * 60)
    print("6. 进制转换")
    print("=" * 60)

    # 十进制 -> 其他进制（Java: Integer.toBinaryString() 等）
    print(f"十进制 255: bin={bin(255)}, oct={oct(255)}, hex={hex(255)}")

    # 其他进制 -> 十进制（Java: Integer.parseInt("ff", 16)）
    print(f"\n其他进制 -> 十进制:")
    print(f"  int('11111111', 2)={int('11111111', 2)}, int('377', 8)={int('377', 8)}")
    print(f"  int('ff', 16)={int('ff', 16)}, int('0xff', 16)={int('0xff', 16)}")

    # 字面量
    print(f"\n字面量: 0b11111111={0b11111111}, 0o377={0o377}, 0xFF={0xFF}")

    # 位运算（和 Java 语法一致）
    a, b = 0b1010, 0b1100
    print(f"\n位运算 (a=0b1010, b=0b1100):")
    print(f"  AND: {bin(a & b)}, OR: {bin(a | b)}, XOR: {bin(a ^ b)}")
    print(f"  NOT: {bin(~a)}, 左移: {bin(a << 2)}, 右移: {bin(a >> 1)}")


# =============================================================================
# 7. 数字格式化
# =============================================================================

def number_formatting_demo():
    """数字格式化 —— f-string 的强大之处"""

    print("\n" + "=" * 60)
    print("7. 数字格式化")
    print("=" * 60)

    # Java: String.format("%,.2f", num)  Python: f"{num:,.2f}"
    num = 1234567.89
    pi = 3.14159265

    # 千分位
    print(f"千分位: {num:,}  下划线: {num:_}")

    # 小数位
    print(f"\n小数位: .2f={pi:.2f}, .4f={pi:.4f}, .10f={pi:.10f}")

    # 百分比
    rate = 0.8567
    print(f"百分比: {rate:.1%}, {rate:.2%}")

    # 宽度与对齐
    print(f"\n对齐（宽度=10）:")
    print(f"  右对齐: [{42:>10}]")
    print(f"  左对齐: [{42:<10}]")
    print(f"  居中:   [{42:^10}]")
    print(f"  零填充: [{42:010}]")

    # 科学计数法
    print(f"\n科学计数法: {6.022e23:.2e}")

    # 综合: 格式化表格
    print(f"\n{'商品':<8} {'单价':>8} {'数量':>4} {'小计':>10}")
    print("-" * 34)
    for name, price, qty in [("Python书", 59.9, 2), ("键盘", 299.0, 1), ("咖啡", 28.5, 5)]:
        print(f"  {name:<8} {price:>8.2f} {qty:>4} {price*qty:>10.2f}")


# =============================================================================
# 8. random 模块基础
# =============================================================================

def random_module_demo():
    """random 模块 vs Java Random/ThreadLocalRandom"""

    print("\n" + "=" * 60)
    print("8. random 模块基础")
    print("=" * 60)

    random.seed(42)                         # 设置种子，便于复现

    # randint: 闭区间 [a, b]（Java: random.nextInt(6) + 1）
    print(f"掷骰子: {random.randint(1, 6)}")

    # random/uniform: 浮点数（Java: random.nextDouble()）
    print(f"随机浮点: {random.random():.4f}")
    print(f"uniform(1, 10): {random.uniform(1, 10):.4f}")

    # choice: 随机选元素（Java 需手动 list.get(random.nextInt(...))）
    colors = ['红', '橙', '黄', '绿', '蓝']
    print(f"随机颜色: {random.choice(colors)}")

    # sample: 不重复抽样
    print(f"彩票号码: {sorted(random.sample(range(1, 36), 5))}")

    # choices: 可重复，可带权重
    weighted = random.choices(['A', 'B', 'C'], weights=[5, 3, 2], k=10)
    print(f"带权重抽样: {weighted}")

    # shuffle: 原地打乱（Java: Collections.shuffle()）
    cards = list(range(1, 11))
    random.shuffle(cards)
    print(f"洗牌: {cards}")

    # randrange: 带步长
    print(f"随机偶数(0-98): {random.randrange(0, 100, 2)}")


# =============================================================================
# 9. 实际场景：金融计算中的精度陷阱
# =============================================================================

def financial_precision_demo():
    """金融计算中的精度陷阱 —— 为什么必须用 Decimal"""

    print("\n" + "=" * 60)
    print("9. 金融计算精度陷阱（实战场景）")
    print("=" * 60)

    # 陷阱 1: float 累加误差
    print("陷阱 1: float 累加误差")
    float_total = sum(0.1 for _ in range(100))
    decimal_total = sum(Decimal('0.1') for _ in range(100))
    print(f"  float:   0.1 * 100 = {float_total}")       # 9.99999999999998
    print(f"  Decimal: 0.1 * 100 = {decimal_total}")     # 10.0

    # 陷阱 2: float 比较
    print(f"\n陷阱 2: float 比较")
    a, b = 0.1 + 0.2, 0.3
    print(f"  float:     0.1 + 0.2 == 0.3 -> {a == b}")               # False
    print(f"  isclose:   -> {math.isclose(a, b)}")                     # True
    print(f"  Decimal:   -> {Decimal('0.1') + Decimal('0.2') == Decimal('0.3')}")

    # 陷阱 3: 金额分摊（100元分3份）
    print(f"\n陷阱 3: 金额分摊（100元分3份）")
    # 错误做法
    float_parts = [round(100.0 / 3, 2)] * 3
    print(f"  float:   {float_parts}, 总和={sum(float_parts)}")    # 99.99!
    # 正确做法：最后一份补差额
    total = Decimal('100.00')
    share = (total / 3).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    parts = [share, share, total - share * 2]
    print(f"  Decimal: {parts}, 总和={sum(parts)}")                # 100.00

    # 陷阱 4: round() 的银行家舍入
    print(f"\n陷阱 4: round() 使用银行家舍入")
    print(f"  round(0.5)={round(0.5)}, round(1.5)={round(1.5)}, "
          f"round(2.5)={round(2.5)}, round(3.5)={round(3.5)}")
    print(f"  注意: 0.5->0, 2.5->2（五取偶，不是四舍五入！）")
    # 传统四舍五入用 Decimal
    val = Decimal('2.5')
    print(f"  Decimal ROUND_HALF_UP: {val} -> "
          f"{val.quantize(Decimal('1'), rounding=ROUND_HALF_UP)}")  # 3

    # 最佳实践总结
    print(f"\n{'=' * 40}")
    print("金融计算最佳实践:")
    print("  1. 用 Decimal('字符串') 创建，不用 Decimal(float)")
    print("  2. 用 quantize() 控制精度，指定舍入模式")
    print("  3. 用 ROUND_HALF_UP 实现传统四舍五入")
    print("  4. 分摊金额时，最后一份用减法补齐")
    print("  5. 永远不要用 == 比较 float")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    builtin_number_types()
    arithmetic_operators()
    math_module_demo()
    decimal_module_demo()
    fractions_demo()
    base_conversion_demo()
    number_formatting_demo()
    random_module_demo()
    financial_precision_demo()
