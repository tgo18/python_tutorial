"""
Python3 函数 —— 写给 Java 开发者

核心差异：
- Python 函数是一等公民（可以赋值、传参、返回）
- Java 8+ 的 Lambda 和方法引用是受限版本的一等公民
- Python 支持 *args, **kwargs 可变参数（比 Java varargs 灵活得多）
- Python 支持多返回值（通过 tuple 解构）
"""


# =============================================================================
# 1. 函数定义与参数
# =============================================================================

def basic_function():
    """基本函数定义"""

    print("=" * 60)
    print("基本函数定义")
    print("=" * 60)

    # Java: public String greet(String name) { return "Hello, " + name; }
    # Python:
    def greet(name):
        return f"Hello, {name}"

    print(greet("张三"))

    # 多返回值（Java 需要自定义类或 Pair）
    def divide(a, b):
        return a // b, a % b    # 返回 tuple

    quotient, remainder = divide(17, 5)
    print(f"17 / 5 = {quotient} 余 {remainder}")

    # 文档字符串（类似 Javadoc）
    def calculate_bmi(weight_kg: float, height_m: float) -> float:
        """
        计算 BMI 指数。

        Args:
            weight_kg: 体重（千克）
            height_m: 身高（米）

        Returns:
            BMI 指数值
        """
        return weight_kg / (height_m ** 2)

    print(f"BMI: {calculate_bmi(70, 1.75):.1f}")
    # help(calculate_bmi)  # 可以查看文档


def parameter_types():
    """参数类型详解"""

    print("\n" + "=" * 60)
    print("参数类型")
    print("=" * 60)

    # 1. 默认参数（Java 不支持，需要方法重载）
    def connect(host, port=3306, timeout=30):
        print(f"  连接 {host}:{port}, 超时={timeout}s")

    connect("localhost")                    # 使用默认值
    connect("localhost", 5432)              # 覆盖 port
    connect("localhost", timeout=60)        # 跳过 port，指定 timeout

    # ⚠️ 陷阱：默认参数是可变对象时的坑
    # BAD:
    def bad_append(item, lst=[]):    # 所有调用共享同一个列表！
        lst.append(item)
        return lst

    print(f"\n  bad: {bad_append(1)}")   # [1]
    print(f"  bad: {bad_append(2)}")     # [1, 2] ← 不是 [2]！

    # GOOD:
    def good_append(item, lst=None):
        if lst is None:
            lst = []
        lst.append(item)
        return lst

    print(f"  good: {good_append(1)}")   # [1]
    print(f"  good: {good_append(2)}")   # [2] ← 正确

    # 2. *args —— 可变位置参数（类似 Java 的 varargs）
    # Java: public void log(String... messages) { ... }
    def log(*messages):
        for msg in messages:
            print(f"  LOG: {msg}")

    print()
    log("启动", "初始化完成", "开始处理")

    # 3. **kwargs —— 可变关键字参数（Java 没有直接对应）
    def create_user(**kwargs):
        print(f"  创建用户: {kwargs}")

    create_user(name="张三", age=30, role="admin")

    # 4. 组合使用
    def api_call(method, url, *args, headers=None, **kwargs):
        print(f"\n  {method} {url}")
        print(f"  args: {args}")
        print(f"  headers: {headers}")
        print(f"  kwargs: {kwargs}")

    api_call("POST", "/api/users", "arg1", headers={"Auth": "token"}, timeout=30)


def positional_keyword_only():
    """仅位置参数 / 仅关键字参数（Python 3.8+）"""

    print("\n" + "=" * 60)
    print("仅位置/仅关键字参数")
    print("=" * 60)

    # / 之前的参数只能按位置传
    # * 之后的参数只能按关键字传
    def example(pos_only, /, normal, *, kw_only):
        print(f"  pos_only={pos_only}, normal={normal}, kw_only={kw_only}")

    example(1, 2, kw_only=3)         # OK
    example(1, normal=2, kw_only=3)  # OK
    # example(pos_only=1, normal=2, kw_only=3)  # TypeError!


# =============================================================================
# 2. 函数作为一等公民
# =============================================================================

def first_class_functions():
    """函数是一等公民"""

    print("\n" + "=" * 60)
    print("函数是一等公民")
    print("=" * 60)

    # 1. 函数赋值给变量
    def square(x):
        return x ** 2

    f = square          # 注意：没有括号，不是调用
    print(f"f(5) = {f(5)}")

    # 2. 函数作为参数（类似 Java 的 Function<T, R> 接口）
    def apply(func, value):
        return func(value)

    print(f"apply(square, 5) = {apply(square, 5)}")

    # 3. 函数作为返回值（工厂模式）
    def make_multiplier(n):
        def multiplier(x):
            return x * n
        return multiplier

    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")

    # 4. 存储在数据结构中
    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }
    print(f"3 + 5 = {operations['+'](3, 5)}")
    print(f"3 * 5 = {operations['*'](3, 5)}")


def lambda_demo():
    """Lambda 表达式"""

    print("\n" + "=" * 60)
    print("Lambda 表达式")
    print("=" * 60)

    # Java: (x, y) -> x + y
    # Python: lambda x, y: x + y（只能是单个表达式）
    add = lambda x, y: x + y
    print(f"lambda add: {add(3, 5)}")

    # 常见用法：排序的 key 函数
    users = [
        {"name": "张三", "age": 30},
        {"name": "李四", "age": 25},
        {"name": "王五", "age": 35},
    ]
    users.sort(key=lambda u: u["age"])
    print(f"按年龄排序: {[u['name'] for u in users]}")

    # map / filter / reduce（类似 Java Stream）
    nums = [1, 2, 3, 4, 5]

    # map —— Java: nums.stream().map(x -> x * 2).collect(toList())
    doubled = list(map(lambda x: x * 2, nums))
    print(f"map: {doubled}")

    # filter —— Java: nums.stream().filter(x -> x % 2 == 0).collect(toList())
    evens = list(filter(lambda x: x % 2 == 0, nums))
    print(f"filter: {evens}")

    # reduce —— Java: nums.stream().reduce(0, Integer::sum)
    from functools import reduce
    total = reduce(lambda a, b: a + b, nums)
    print(f"reduce: {total}")

    # 但 Python 风格更推荐列表推导式
    doubled_pythonic = [x * 2 for x in nums]
    evens_pythonic = [x for x in nums if x % 2 == 0]
    total_pythonic = sum(nums)
    print(f"\nPythonic 方式更推荐:")
    print(f"  doubled: {doubled_pythonic}")
    print(f"  evens: {evens_pythonic}")
    print(f"  total: {total_pythonic}")


def closure_demo():
    """闭包"""

    print("\n" + "=" * 60)
    print("闭包")
    print("=" * 60)

    # Java 闭包限制：捕获的变量必须是 effectively final
    # Python 闭包：可以通过 nonlocal 修改外部变量

    def counter(initial=0):
        count = initial

        def increment():
            nonlocal count
            count += 1
            return count

        def decrement():
            nonlocal count
            count -= 1
            return count

        def get():
            return count

        # 返回多个函数，共享同一个 count 变量
        return increment, decrement, get

    inc, dec, get = counter(10)
    print(f"初始: {get()}")
    print(f"加两次: {inc()}, {inc()}")
    print(f"减一次: {dec()}")
    print(f"最终: {get()}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    basic_function()
    parameter_types()
    positional_keyword_only()
    first_class_functions()
    lambda_demo()
    closure_demo()
