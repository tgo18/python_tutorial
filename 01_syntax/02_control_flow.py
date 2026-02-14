"""
Python3 控制流 —— 写给 Java 开发者

核心差异：
- Python 用缩进代替 {}，没有 switch（3.10+ 有 match-case）
- for 循环是 for-each 风格，没有传统的 for(i=0; i<n; i++)
- Python 有海象运算符 :=（Java 没有）
"""


# =============================================================================
# 1. 条件语句
# =============================================================================

def if_else_demo():
    """if-elif-else"""

    print("=" * 60)
    print("条件语句")
    print("=" * 60)

    score = 85

    # Java: if (score >= 90) { ... } else if (score >= 80) { ... }
    # Python: 没有花括号，用缩进；elif 不是 else if
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"

    print(f"score={score}, grade={grade}")

    # 三元表达式
    # Java: String result = score >= 60 ? "PASS" : "FAIL";
    # Python:
    result = "PASS" if score >= 60 else "FAIL"
    print(f"result={result}")

    # 链式比较（Java 没有）
    x = 5
    print(f"1 < x < 10: {1 < x < 10}")          # True，等价于 1 < x and x < 10
    print(f"1 < x < 3: {1 < x < 3}")             # False


def match_case_demo():
    """match-case (Python 3.10+) —— 类似 Java 的增强 switch"""

    print("\n" + "=" * 60)
    print("match-case (结构化模式匹配)")
    print("=" * 60)

    # 比 Java switch 强大得多，支持解构匹配
    def handle_command(command):
        match command.split():
            case ["quit"]:
                return "退出程序"
            case ["hello", name]:
                return f"你好, {name}!"
            case ["add", x, y]:
                return f"结果: {int(x) + int(y)}"
            case ["move", ("up" | "down" | "left" | "right") as direction]:
                return f"移动方向: {direction}"
            case _:
                return f"未知命令: {command}"

    commands = ["quit", "hello 张三", "add 3 5", "move up", "unknown cmd"]
    for cmd in commands:
        print(f"  '{cmd}' -> {handle_command(cmd)}")

    # 匹配数据结构
    def describe_point(point):
        match point:
            case (0, 0):
                return "原点"
            case (x, 0):
                return f"X轴上, x={x}"
            case (0, y):
                return f"Y轴上, y={y}"
            case (x, y) if x == y:
                return f"对角线上, x=y={x}"
            case (x, y):
                return f"普通点 ({x}, {y})"

    points = [(0, 0), (3, 0), (0, 5), (4, 4), (1, 2)]
    for p in points:
        print(f"  {p} -> {describe_point(p)}")


# =============================================================================
# 2. 循环
# =============================================================================

def loop_demo():
    """循环语句"""

    print("\n" + "=" * 60)
    print("循环语句")
    print("=" * 60)

    # --- for 循环 ---
    # Java: for (int i = 0; i < 5; i++) { ... }
    # Python: for i in range(5)
    print("range(5):", end=" ")
    for i in range(5):          # [0, 1, 2, 3, 4]
        print(i, end=" ")
    print()

    print("range(2, 8):", end=" ")
    for i in range(2, 8):       # [2, 3, 4, 5, 6, 7]
        print(i, end=" ")
    print()

    print("range(0, 10, 3):", end=" ")
    for i in range(0, 10, 3):   # [0, 3, 6, 9] 步长为3
        print(i, end=" ")
    print()

    # 遍历列表
    # Java: for (String fruit : fruits) { ... }
    fruits = ["apple", "banana", "cherry"]
    for fruit in fruits:
        print(f"  水果: {fruit}")

    # 带索引遍历
    # Java: for (int i = 0; i < fruits.size(); i++) { ... }
    # Python: 不要用 range(len(...))，用 enumerate
    for idx, fruit in enumerate(fruits):
        print(f"  [{idx}] {fruit}")

    # 同时遍历多个列表
    # Java: 需要索引或 IntStream.range
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    for name, age in zip(names, ages):
        print(f"  {name}: {age}岁")

    # 遍历字典
    user = {"name": "张三", "age": 30, "city": "北京"}
    for key, value in user.items():
        print(f"  {key}: {value}")


def for_else_demo():
    """for-else —— Python 独有的语法"""

    print("\n" + "=" * 60)
    print("for-else 语句")
    print("=" * 60)

    # Java 中需要额外的 boolean 标志
    # Python 的 for-else: else 块在循环 正常完成（没有 break）时执行

    # 示例：查找质数
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                break
        else:
            # 没有执行 break，说明没找到因子 -> 是质数
            return True
        return False

    primes = [n for n in range(2, 30) if is_prime(n)]
    print(f"30以内的质数: {primes}")


def while_demo():
    """while 循环"""

    print("\n" + "=" * 60)
    print("while 循环")
    print("=" * 60)

    # 基本 while
    count = 0
    while count < 5:
        print(f"  count = {count}")
        count += 1
    # 注意: Python 没有 do-while

    # 海象运算符 := (Python 3.8+)
    # 在表达式中赋值，减少重复计算
    print("\n海象运算符 :=")
    data = [1, 5, 3, 8, 2, 9, 4]
    # 不用海象运算符
    # filtered = []
    # for x in data:
    #     y = x ** 2
    #     if y > 10:
    #         filtered.append(y)
    # 用海象运算符（更简洁）
    filtered = [y for x in data if (y := x ** 2) > 10]
    print(f"  平方大于10的: {filtered}")

    # while 中使用海象运算符
    import io
    reader = io.StringIO("line1\nline2\nline3\n")
    while (line := reader.readline()):
        print(f"  读取: {line.strip()}")


# =============================================================================
# 3. 迭代工具
# =============================================================================

def iteration_tools():
    """实用迭代工具"""

    print("\n" + "=" * 60)
    print("迭代工具")
    print("=" * 60)

    # reversed —— 反向迭代
    for i in reversed(range(5)):
        print(i, end=" ")
    print()

    # sorted —— 排序（返回新列表）
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"升序: {sorted(nums)}")
    print(f"降序: {sorted(nums, reverse=True)}")
    print(f"原列表不变: {nums}")

    # 自定义排序（类似 Java Comparator）
    words = ["banana", "apple", "cherry", "date"]
    print(f"按长度排序: {sorted(words, key=len)}")
    print(f"按末尾字母: {sorted(words, key=lambda w: w[-1])}")

    # any / all —— 类似 Java Stream 的 anyMatch / allMatch
    nums = [2, 4, 6, 8, 10]
    print(f"\nall 偶数: {all(n % 2 == 0 for n in nums)}")
    print(f"any 大于5: {any(n > 5 for n in nums)}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    if_else_demo()
    match_case_demo()
    loop_demo()
    for_else_demo()
    while_demo()
    iteration_tools()
