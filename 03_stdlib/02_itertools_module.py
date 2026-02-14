"""
Python3 itertools 模块 —— 写给 Java 开发者

核心概念：
- itertools 是 Python 的"迭代器工具箱"，全部惰性求值
- 类比 Java: Stream API 的 Python 版本，但功能更丰富
"""

import itertools
import operator


# =============================================================================
# 1. 无限迭代器: count, cycle, repeat
# =============================================================================

def infinite_iterators_demo():
    """无限迭代器 vs Java Stream.iterate/generate"""

    print("=" * 60)
    print("无限迭代器: count, cycle, repeat")
    print("=" * 60)

    # --- count: 无限计数器 ---
    # Java: IntStream.iterate(0, i -> i + 1) 或 Stream.iterate(0, i -> i + 2)
    counter = itertools.count(start=0, step=2)
    print(f"count(0, 2) 前5个: {[next(counter) for _ in range(5)]}")

    # 可以用浮点步长（Java IntStream 做不到）
    float_counter = itertools.count(0.0, 0.5)
    print(f"count(0.0, 0.5) 前5个: {[next(float_counter) for _ in range(5)]}")

    # 常见用法：给序列编号（类似 Java 的 IntStream.range + zip）
    names = ["Alice", "Bob", "Charlie"]
    print(f"编号: {list(zip(itertools.count(1), names))}")

    # --- cycle: 无限循环 ---
    # Java: 没有直接对应，需要 Stream.generate(() -> list.get(i++ % size))
    colors = itertools.cycle(["红", "绿", "蓝"])
    print(f"\ncycle 前7个: {[next(colors) for _ in range(7)]}")

    # 实用场景：轮询分配任务
    servers = itertools.cycle(["server-A", "server-B", "server-C"])
    tasks = [f"task-{i}" for i in range(6)]
    print(f"轮询分配: {dict(zip(tasks, servers))}")

    # --- repeat: 重复元素 ---
    # Java: Stream.generate(() -> value).limit(n)
    print(f"\nrepeat('hello', 3): {list(itertools.repeat('hello', 3))}")

    # 配合 map 使用（类似 Java Stream.map）
    powers = list(map(pow, range(5), itertools.repeat(2)))
    print(f"map(pow, range(5), repeat(2)): {powers}")  # [0, 1, 4, 9, 16]


# =============================================================================
# 2. 终止迭代器: chain, islice, takewhile, dropwhile, groupby
# =============================================================================

def terminating_iterators_demo():
    """终止迭代器 —— 处理有限序列"""

    print("\n" + "=" * 60)
    print("终止迭代器: chain, islice, takewhile, dropwhile, groupby")
    print("=" * 60)

    # --- chain: 串联多个可迭代对象 ---
    # Java: Stream.concat(s1, s2) 或 Stream.of(s1,s2).flatMap(s -> s)
    chained = list(itertools.chain([1, 2, 3], [4, 5, 6], [7, 8, 9]))
    print(f"chain: {chained}")

    # chain.from_iterable: 展开嵌套列表（类似 Java flatMap）
    nested = [[1, 2], [3, 4], [5, 6]]
    print(f"chain.from_iterable (flatMap): {list(itertools.chain.from_iterable(nested))}")

    # --- islice: 切片迭代器 ---
    # Java: Stream.skip(n).limit(m)
    # 对无限迭代器安全切片（不能用普通切片 [:]）
    natural = itertools.count(1)
    print(f"\nislice(count(1), 5, 10): {list(itertools.islice(natural, 5, 10))}")

    # 带步长：斐波那契隔一个取一个
    fib_gen = _fibonacci_gen()
    print(f"斐波那契隔一个取一个: {list(itertools.islice(fib_gen, 0, 10, 2))}")

    # --- takewhile / dropwhile ---
    # Java: Stream.takeWhile / dropWhile（Java 9+）
    data = [2, 4, 6, 7, 8, 10]
    print(f"\ntakewhile(偶数, {data}): "
          f"{list(itertools.takewhile(lambda x: x % 2 == 0, data))}")
    print(f"dropwhile(偶数, {data}): "
          f"{list(itertools.dropwhile(lambda x: x % 2 == 0, data))}")

    # --- groupby: 分组 ---
    # Java: Collectors.groupingBy()（但 itertools.groupby 要求数据已排序！）
    print(f"\n--- groupby（必须先排序！）---")
    animals = [
        ("cat", "哺乳"), ("dog", "哺乳"), ("snake", "爬行"),
        ("eagle", "鸟类"), ("lizard", "爬行"), ("parrot", "鸟类"),
    ]
    animals.sort(key=lambda x: x[1])  # 必须先排序！与 Java groupingBy 最大差异

    for category, group in itertools.groupby(animals, key=lambda x: x[1]):
        print(f"  {category}: {[name for name, _ in group]}")

    # 连续相同元素分组（groupby 的原始用途）
    data = "AAABBBCCDDDDEE"
    groups = [(k, len(list(g))) for k, g in itertools.groupby(data)]
    print(f"连续字符统计 '{data}': {groups}")


def _fibonacci_gen():
    """斐波那契生成器（辅助函数）"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# =============================================================================
# 3. 组合迭代器: product, permutations, combinations
# =============================================================================

def combinatoric_iterators_demo():
    """组合迭代器 —— Java 中没有直接对应，通常需要手写多重循环"""

    print("\n" + "=" * 60)
    print("组合迭代器: product, permutations, combinations")
    print("=" * 60)

    # --- product: 笛卡尔积 ---
    # Java: 需要嵌套 for 循环
    colors = ["红", "蓝"]
    sizes = ["S", "M", "L"]
    combos = list(itertools.product(colors, sizes))
    print(f"product(颜色, 尺码): {[f'{c}-{s}' for c, s in combos]}")

    # repeat 参数：自身的笛卡尔积（等价于多个 range(2) 的 product）
    binary = list(itertools.product(range(2), repeat=3))
    print(f"3位二进制: {binary}")

    # --- permutations: 排列 ---
    # Java: 无内置，需要递归或库
    items = ["A", "B", "C"]
    perms = list(itertools.permutations(items))
    print(f"\npermutations({items}): 共 {len(perms)} 种")
    print(f"  {perms}")

    perms_2 = list(itertools.permutations(items, 2))
    print(f"permutations({items}, 2): {perms_2}")

    # --- combinations: 组合（不重复）---
    combs = list(itertools.combinations(items, 2))
    print(f"\ncombinations({items}, 2): {combs}")

    # --- combinations_with_replacement: 可重复组合 ---
    combs_r = list(itertools.combinations_with_replacement(items, 2))
    print(f"combinations_with_replacement({items}, 2): {combs_r}")

    # 实际应用：生成所有可能的查询条件组合
    fields = ["name", "age", "city"]
    total = sum(1 for r in range(1, len(fields) + 1)
                for _ in itertools.combinations(fields, r))
    print(f"\n查询字段组合数: {total}")


# =============================================================================
# 4. accumulate —— 类似 Java Stream.reduce 但保留中间结果
# =============================================================================

def accumulate_demo():
    """accumulate: 累积计算，保留每一步的中间结果"""

    print("\n" + "=" * 60)
    print("accumulate: 累积计算")
    print("=" * 60)

    # --- 累加（默认行为）---
    # Java Stream.reduce 只返回最终结果; Python accumulate 返回所有中间结果
    nums = [1, 2, 3, 4, 5]
    print(f"累加 {nums}: {list(itertools.accumulate(nums))}")

    # --- 累乘 ---
    print(f"累乘 {nums}: {list(itertools.accumulate(nums, operator.mul))}")

    # --- 自定义函数：累积最大值 / 最小值 ---
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"累积最大值 {data}: {list(itertools.accumulate(data, max))}")
    print(f"累积最小值 {data}: {list(itertools.accumulate(data, min))}")

    # --- 带初始值（Python 3.8+）---
    result = list(itertools.accumulate(nums, operator.add, initial=100))
    print(f"带初始值(100) 累加: {result}")
    # 对比 Java:
    # Java Stream.reduce(100, Integer::sum) -> 单个结果 115
    # Python accumulate(..., initial=100) -> [100, 101, 103, 106, 110, 115]
    print("  Java reduce 只返回最终值; Python accumulate 返回全部中间值")


# =============================================================================
# 5. zip_longest
# =============================================================================

def zip_longest_demo():
    """zip_longest: 不丢弃较长序列的元素"""

    print("\n" + "=" * 60)
    print("zip_longest")
    print("=" * 60)

    # 内置 zip 按最短截断
    names = ["Alice", "Bob", "Charlie", "Diana"]
    scores = [90, 85, 78]
    print(f"zip (截断): {list(zip(names, scores))}")

    # zip_longest 用填充值补齐
    # Java: 无直接对应，需手动处理长度差异
    print(f"zip_longest (填充0): "
          f"{list(itertools.zip_longest(names, scores, fillvalue=0))}")
    print(f"zip_longest (默认None): "
          f"{list(itertools.zip_longest(names, scores))}")

    # 实用：合并多个数据源对齐展示
    headers = ["姓名", "年龄", "城市"]
    row1 = ["张三", 30]
    row2 = ["李四", 25, "北京"]
    for header, v1, v2 in itertools.zip_longest(headers, row1, row2, fillvalue="-"):
        print(f"  {header}: {v1} | {v2}")


# =============================================================================
# 6. 实际应用场景（数据处理管道）
# =============================================================================

def data_pipeline_demo():
    """用 itertools 构建数据处理管道 —— 全部惰性求值"""

    print("\n" + "=" * 60)
    print("实际应用：数据处理管道")
    print("=" * 60)

    # 模拟日志数据
    logs = [
        "2024-01-01 INFO  用户登录: alice",
        "2024-01-01 ERROR 数据库连接超时",
        "2024-01-01 INFO  用户登录: bob",
        "2024-01-02 WARN  内存使用率高",
        "2024-01-02 ERROR 服务不可用",
        "2024-01-02 INFO  用户登出: alice",
        "2024-01-03 ERROR 磁盘空间不足",
        "2024-01-03 INFO  用户登录: charlie",
    ]

    # --- 管道1: 过滤 + 限制 ---
    # Java: logs.stream().filter(...).limit(2)
    error_logs = itertools.islice(
        (log for log in logs if "ERROR" in log), 2
    )
    print("--- 前2条错误日志 ---")
    for log in error_logs:
        print(f"  {log}")

    # --- 管道2: 按日期分组统计 ---
    # Java: Collectors.groupingBy(log -> log.substring(0, 10), Collectors.counting())
    sorted_logs = sorted(logs, key=lambda l: l[:10])
    print("\n--- 按日期分组 ---")
    for date, group in itertools.groupby(sorted_logs, key=lambda l: l[:10]):
        print(f"  {date}: {len(list(group))} 条日志")

    # --- 管道3: 多来源数据合并 + 排序取 Top3 ---
    source_a = [("user1", 100), ("user2", 200)]
    source_b = [("user3", 150), ("user4", 300)]
    source_c = [("user5", 250)]

    all_users = itertools.chain(source_a, source_b, source_c)
    top3 = itertools.islice(
        sorted(all_users, key=lambda x: x[1], reverse=True), 3
    )
    print("\n--- 合并多来源取 Top3 ---")
    for name, amount in top3:
        print(f"  {name}: {amount}")

    # --- 管道4: 滑动窗口计算移动平均 ---
    def sliding_window(iterable, n):
        """滑动窗口实现"""
        it = iter(iterable)
        window = list(itertools.islice(it, n))
        if len(window) == n:
            yield tuple(window)
        for item in it:
            window = window[1:] + [item]
            yield tuple(window)

    prices = [100, 102, 98, 105, 110, 108, 112]
    print(f"\n--- 价格滑动窗口(3) ---")
    for window in sliding_window(prices, 3):
        print(f"  {window} -> 均值: {sum(window) / len(window):.1f}")

    # --- 管道5: 用 accumulate 做累积统计 ---
    daily_sales = [120, 85, 200, 150, 90, 310, 175]
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    print(f"\n--- 每日累积销售额 ---")
    cumulative = itertools.accumulate(daily_sales)
    for day, daily, total in zip(days, daily_sales, cumulative):
        bar = "#" * (daily // 20)
        print(f"  {day}: {daily:>3} (累计: {total:>4}) {bar}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    infinite_iterators_demo()
    terminating_iterators_demo()
    combinatoric_iterators_demo()
    accumulate_demo()
    zip_longest_demo()
    data_pipeline_demo()
