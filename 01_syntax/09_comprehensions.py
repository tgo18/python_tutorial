"""
Python3 推导式 —— 写给 Java 开发者

核心概念：
- 推导式是 Python 最优雅的语法糖之一
- 类比 Java: Stream API 的 map/filter/collect，但语法更简洁
- 一行代码完成 Java 需要 3-5 行的操作
"""

import sys
import time
from collections import defaultdict


# ============================================================
# 1. 列表推导式 —— 对比 Java Stream.map().collect()
# ============================================================

def list_comprehension_demo():
    """列表推导式基础"""
    print("=" * 60)
    print("列表推导式 (List Comprehension)")
    print("=" * 60)

    # Java: numbers.stream().map(x -> x * x).collect(Collectors.toList());
    # Python: [表达式 for 变量 in 可迭代对象]
    numbers = [1, 2, 3, 4, 5]
    squares = [x * x for x in numbers]
    print(f"  平方: {squares}")

    # 等价的传统写法（推导式是它的语法糖）
    squares_loop = []
    for x in numbers:
        squares_loop.append(x * x)

    # 字符串处理 & 类型转换
    names = ["alice", "bob", "charlie"]
    print(f"  大写: {[name.upper() for name in names]}")
    print(f"  转整数: {[int(s) for s in ['10', '20', '30']]}")
    print(f"  长度: {[len(name) for name in names]}")


# ============================================================
# 2. 带条件的推导式 —— 对比 Java Stream.filter()
# ============================================================

def filtered_comprehension_demo():
    """带过滤条件的推导式"""
    print("\n" + "=" * 60)
    print("带条件的推导式 (filter)")
    print("=" * 60)

    # Java: numbers.stream().filter(x -> x % 2 == 0).collect(...)
    # Python: [表达式 for 变量 in 可迭代对象 if 条件]
    numbers = range(1, 21)
    print(f"  偶数: {[x for x in numbers if x % 2 == 0]}")
    print(f"  偶数的平方: {[x * x for x in numbers if x % 2 == 0]}")
    print(f"  被3和5整除: {[x for x in range(1, 31) if x % 3 == 0 and x % 5 == 0]}")

    # 条件表达式（三元运算符）—— 注意: 这是 map，不是 filter
    labels = ["偶" if x % 2 == 0 else "奇" for x in range(1, 6)]
    print(f"  奇偶标签: {labels}")

    # filter + 条件表达式组合
    words = ["hello", "", "world", "", "python"]
    print(f"  非空大写: {[w.upper() for w in words if w]}")


# ============================================================
# 3. 嵌套推导式 —— 对比 Java flatMap
# ============================================================

def nested_comprehension_demo():
    """嵌套推导式"""
    print("\n" + "=" * 60)
    print("嵌套推导式 (flatMap)")
    print("=" * 60)

    # Java: matrix.stream().flatMap(Collection::stream).collect(...)
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [x for row in matrix for x in row]
    print(f"  扁平化: {flat}")
    # 阅读顺序和循环一致: for row in matrix -> for x in row

    # 笛卡尔积
    combos = [(c, s) for c in ["红", "蓝"] for s in ["S", "M", "L"]]
    print(f"  组合: {combos}")

    # 嵌套推导式生成二维结构: 3x3 单位矩阵
    identity = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    print(f"  单位矩阵:")
    for row in identity:
        print(f"    {row}")
    # 提示: 超过两层嵌套时，用普通 for 循环更可读


# ============================================================
# 4. 字典推导式 —— 对比 Java Collectors.toMap()
# ============================================================

def dict_comprehension_demo():
    """字典推导式"""
    print("\n" + "=" * 60)
    print("字典推导式 (Dict Comprehension)")
    print("=" * 60)

    # Java: names.stream().collect(Collectors.toMap(n -> n, String::length));
    # Python: {key: value for 变量 in 可迭代对象}
    names = ["alice", "bob", "charlie"]
    name_lengths = {name: len(name) for name in names}
    print(f"  名字长度: {name_lengths}")

    # 键值互换
    original = {"a": 1, "b": 2, "c": 3}
    print(f"  键值互换: {({v: k for k, v in original.items()})}")

    # 带过滤
    scores = {"alice": 85, "bob": 62, "charlie": 91, "david": 58}
    passed = {name: score for name, score in scores.items() if score >= 70}
    print(f"  及格的: {passed}")

    # 从两个列表构建字典（类似 Java 的 zip + toMap）
    person = {k: v for k, v in zip(["name", "age", "city"], ["张三", 30, "北京"])}
    print(f"  构建字典: {person}")

    # 分数等级转换
    grades = {
        name: ("优" if s >= 90 else "良" if s >= 70 else "差")
        for name, s in scores.items()
    }
    print(f"  等级: {grades}")


# ============================================================
# 5. 集合推导式
# ============================================================

def set_comprehension_demo():
    """集合推导式"""
    print("\n" + "=" * 60)
    print("集合推导式 (Set Comprehension)")
    print("=" * 60)

    # 语法: {表达式 for 变量 in 可迭代对象}  （没有冒号，区别于字典推导式）
    words = ["hello", "world", "hello", "python", "world"]
    print(f"  不重复的长度: {({len(w) for w in words})}")

    # 提取首字母（自动去重）
    names = ["alice", "anna", "bob", "bella", "charlie"]
    initials = {name[0].upper() for name in names}
    print(f"  首字母集合: {sorted(initials)}")

    # 两个列表的共同元素的平方
    a, b = [1, 2, 3, 4, 5], [3, 4, 5, 6, 7]
    common_squares = {x * x for x in a if x in set(b)}
    print(f"  共同元素平方: {common_squares}")


# ============================================================
# 6. 生成器表达式 —— 惰性求值，内存友好
# ============================================================

def generator_expression_demo():
    """生成器表达式（圆括号版推导式）"""
    print("\n" + "=" * 60)
    print("生成器表达式 (Generator Expression)")
    print("=" * 60)

    # [x for x in ...] 立即生成所有元素，占内存
    # (x for x in ...) 惰性求值，按需生成
    # Java 类比: Stream 本身就是惰性的，collect 才触发求值
    list_comp = [x * x for x in range(10)]
    gen_exp = (x * x for x in range(10))
    print(f"  列表推导式: {list_comp} -> {type(list_comp).__name__}")
    print(f"  生成器对象: {gen_exp}")
    print(f"  转为列表:   {list(gen_exp)}")

    # 直接传给函数时，可省略外层括号
    print(f"  1~10 平方和: {sum(x * x for x in range(1, 11))}")
    print(f"  最长单词长度: {max(len(w) for w in ['python', 'java', 'go'])}")
    print(f"  包含负数: {any(x < 0 for x in [1, -2, 3])}")
    print(f"  全部为正: {all(x > 0 for x in [1, 2, 3])}")

    # 内存对比: 处理大数据时差异巨大
    list_size = sys.getsizeof([x for x in range(10000)])
    gen_size = sys.getsizeof(x for x in range(10000))
    print(f"\n  列表 (10000元素) 内存: {list_size:,} bytes")
    print(f"  生成器 (10000元素) 内存: {gen_size:,} bytes")


# ============================================================
# 7. 推导式 vs map/filter —— 何时用哪个
# ============================================================

def comprehension_vs_map_filter_demo():
    """推导式与 map/filter 的对比"""
    print("\n" + "=" * 60)
    print("推导式 vs map/filter")
    print("=" * 60)

    numbers = [1, 2, 3, 4, 5]

    # --- map 对比 ---
    print(f"  推导式平方: {[x ** 2 for x in numbers]}")
    print(f"  map 平方:   {list(map(lambda x: x ** 2, numbers))}")
    # map + 已有函数时，map 更简洁
    print(f"  map(str):   {list(map(str, numbers))}")
    print(f"  推导str:    {[str(x) for x in numbers]}")

    # --- filter 对比 ---
    print(f"  推导式偶数: {[x for x in numbers if x % 2 == 0]}")
    print(f"  filter偶数: {list(filter(lambda x: x % 2 == 0, numbers))}")

    # --- 选择建议 ---
    print(f"\n  何时用推导式: map+filter 组合时 / 表达式简单时")
    print(f"  何时用 map:   已有现成函数 map(int, strings)")


# ============================================================
# 8. 实际应用场景（数据转换、过滤、分组）
# ============================================================

def practical_examples_demo():
    """实际开发中的推导式应用"""
    print("\n" + "=" * 60)
    print("实际应用场景")
    print("=" * 60)

    # --- 场景1: 数据清洗 ---
    print("--- 数据清洗 ---")
    raw_data = ["  Alice  ", "BOB", "", "  charlie ", None, "David"]
    cleaned = [s.strip().title() for s in raw_data if s and s.strip()]
    print(f"  清洗后: {cleaned}")

    # --- 场景2: JSON 数据提取（常见于 API 开发）---
    print("\n--- 数据提取 ---")
    users = [
        {"name": "alice", "age": 25, "active": True},
        {"name": "bob", "age": 30, "active": False},
        {"name": "charlie", "age": 35, "active": True},
    ]
    print(f"  活跃用户: {[u['name'] for u in users if u['active']]}")
    name_age = {u["name"]: u["age"] for u in users}
    print(f"  姓名年龄: {name_age}")

    # --- 场景3: 分组（类似 Java Collectors.groupingBy）---
    print("\n--- 分组 ---")
    words = ["apple", "ant", "banana", "bear", "cat", "cherry"]
    by_first = defaultdict(list)
    for w in words:
        by_first[w[0]].append(w)
    grouped = {k: v for k, v in sorted(by_first.items())}
    print(f"  按首字母分组: {grouped}")

    # --- 场景4: 矩阵转置 ---
    print("\n--- 矩阵转置 ---")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print(f"  原矩阵: {matrix}")
    print(f"  转置后: {transposed}")


# ============================================================
# 9. 性能对比和最佳实践（何时不该用推导式）
# ============================================================

def performance_and_best_practices_demo():
    """性能对比和最佳实践"""
    print("\n" + "=" * 60)
    print("性能对比和最佳实践")
    print("=" * 60)

    # --- 性能对比 ---
    print("--- 性能对比 (50万次求平方和) ---")
    n = 500_000

    start = time.perf_counter()
    r1 = sum([x * x for x in range(n)])
    t1 = time.perf_counter() - start
    start = time.perf_counter()
    r2 = sum(x * x for x in range(n))
    t2 = time.perf_counter() - start
    start = time.perf_counter()
    r3 = 0
    for x in range(n):
        r3 += x * x
    t3 = time.perf_counter() - start

    print(f"  列表推导式:   {t1:.4f}s")
    print(f"  生成器表达式: {t2:.4f}s")
    print(f"  for 循环:     {t3:.4f}s")
    assert r1 == r2 == r3

    # --- 最佳实践 ---
    print(f"\n--- 最佳实践 ---")
    print("  [规则1] 保持简单，超过一行就拆开")
    print("  [规则2] 不要用推导式执行副作用")
    # 不好: [print(x) for x in range(5)]  # 滥用，结果被丢弃
    # 好:   for x in range(5): print(x)
    print("  [规则3] 大数据用生成器表达式，避免内存爆炸")
    # 不好: sum([x for x in range(10_000_000)])
    # 好:   sum(x for x in range(10_000_000))

    print("  [规则4] 选择合适的推导式类型")
    data = [1, 2, 2, 3, 3, 3]
    as_list = [x * 2 for x in data]
    as_set = {x * 2 for x in data}
    as_dict = {x: x * 2 for x in data}
    print(f"    需要列表 -> []: {as_list}")
    print(f"    需要去重 -> {{}}: {as_set}")
    print(f"    需要映射 -> {{k:v}}: {as_dict}")

    # walrus 运算符 (:=) 避免重复计算 (Python 3.8+)
    print("\n  [规则5] 用 := 避免重复计算")
    data = ["hello world", "hi", "good morning everyone", "ok"]
    long_upper = [upper for s in data if len(upper := s.upper()) > 5]
    print(f"    长字符串大写: {long_upper}")


# ============================================================
# 运行所有 demo
# ============================================================

if __name__ == "__main__":
    list_comprehension_demo()
    filtered_comprehension_demo()
    nested_comprehension_demo()
    dict_comprehension_demo()
    set_comprehension_demo()
    generator_expression_demo()
    comprehension_vs_map_filter_demo()
    practical_examples_demo()
    performance_and_best_practices_demo()
