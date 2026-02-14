"""
Python3 类型与变量 —— 写给 Java 开发者

核心差异：
- Java: 静态类型，变量声明时必须指定类型
- Python: 动态类型，变量是"标签"贴在对象上，不是"盒子"装对象

Java 思维:  int x = 10;     // x 是一个 int 类型的盒子，里面装着 10
Python 思维: x = 10          # x 是一个标签，贴在整数对象 10 上
"""


# =============================================================================
# 1. 基本数据类型
# =============================================================================

def basic_types():
    """Python 基本类型 vs Java 基本类型"""

    # --- 数值类型 ---
    # Java: int, long, float, double 有精度区分
    # Python: int 无限精度，float 对应 Java 的 double
    i = 42                      # int（无限精度，不会溢出！）
    big = 10 ** 100             # Java 需要 BigInteger，Python 原生支持
    f = 3.14                    # float（64位双精度，相当于 Java double）
    c = 3 + 4j                  # complex 复数（Java 无原生支持）
    b = True                    # bool（True/False，注意大写）

    print(f"int: {i}, type: {type(i)}")
    print(f"大整数: {big}, type: {type(big)}")
    print(f"float: {f}, type: {type(f)}")
    print(f"complex: {c}, type: {type(c)}")
    print(f"bool: {b}, type: {type(b)}")

    # 数值运算
    print(f"\n// 除法（Java 思维陷阱）")
    print(f"10 / 3 = {10 / 3}")       # 2.0 —— 真除法（Java 中 10/3=3）
    print(f"10 // 3 = {10 // 3}")     # 3 —— 整除（等价于 Java 的 10/3）
    print(f"10 % 3 = {10 % 3}")       # 1 —— 取模
    print(f"2 ** 10 = {2 ** 10}")     # 1024 —— 幂运算（Java 用 Math.pow）

    # --- 字符串 ---
    # Java: String 是类，用 "" 包裹
    # Python: str 是类，'' 和 "" 等价，还有 ''' 和 f-string
    s1 = 'hello'                # 单引号
    s2 = "hello"                # 双引号（与单引号完全等价）
    s3 = """多行
字符串"""                        # 三引号（Java 15+ 的 Text Block）
    s4 = f"value is {i}"        # f-string（Java 没有，最接近的是 String.format）

    print(f"\n字符串: {s1}, {s4}")
    print(f"切片: {'hello world'[0:5]}")    # hello（Java 用 substring）
    print(f"反转: {'hello'[::-1]}")          # olleh（Java 没有直接方式）

    # 字符串是不可变的（和 Java 的 String 一样）
    # s1[0] = 'H'  # TypeError!

    # --- None ---
    # Java: null
    # Python: None（是一个单例对象，不是关键字）
    x = None
    print(f"\nNone: {x}, type: {type(x)}")
    print(f"x is None: {x is None}")   # 用 is 判断，不用 ==


def container_types():
    """容器类型 vs Java 集合框架"""

    print("\n" + "=" * 60)
    print("容器类型")
    print("=" * 60)

    # --- list（列表）---
    # Java: ArrayList<Object>，但 Python 的 list 可混合类型
    nums = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, None]   # Java 中需要 List<Object>

    # 列表操作
    nums.append(6)                      # add()
    nums.extend([7, 8])                 # addAll()
    nums.insert(0, 0)                   # add(index, element)
    popped = nums.pop()                 # removeLast()
    print(f"list: {nums}")
    print(f"切片: {nums[2:5]}")         # subList(2, 5)
    print(f"长度: {len(nums)}")         # size()
    print(f"包含: {3 in nums}")         # contains()

    # 列表是可变的
    nums[0] = 100
    print(f"修改后: {nums}")

    # --- tuple（元组）---
    # Java 无直接对应（最接近的是不可变的 Record 或 Pair）
    # 不可变的有序序列
    point = (3, 4)
    rgb = (255, 128, 0)

    x, y = point                        # 解构赋值（Java 17+ Record 的解构）
    print(f"\ntuple: {point}, x={x}, y={y}")

    # 单元素 tuple 需要逗号
    single = (42,)                      # 不是 (42)
    print(f"单元素 tuple: {single}, type: {type(single)}")

    # --- dict（字典）---
    # Java: HashMap<K, V>
    user = {
        "name": "张三",
        "age": 30,
        "skills": ["Java", "Python"]
    }

    print(f"\ndict: {user}")
    print(f"取值: {user['name']}")              # get("name") 但不存在会抛异常
    print(f"安全取值: {user.get('email', 'N/A')}")  # getOrDefault()
    user["email"] = "zhangsan@test.com"          # put()
    print(f"keys: {list(user.keys())}")          # keySet()
    print(f"values: {list(user.values())}")      # values()
    print(f"items: {list(user.items())}")        # entrySet()

    # 字典推导式（后面详细讲）
    squares = {x: x**2 for x in range(5)}
    print(f"推导式: {squares}")

    # --- set（集合）---
    # Java: HashSet<E>
    s1 = {1, 2, 3, 4}
    s2 = {3, 4, 5, 6}

    print(f"\nset 交集: {s1 & s2}")             # intersection
    print(f"set 并集: {s1 | s2}")               # union
    print(f"set 差集: {s1 - s2}")               # difference
    print(f"set 对称差集: {s1 ^ s2}")           # symmetric difference

    # 空 set 必须用 set()，因为 {} 是空字典
    empty_set = set()
    empty_dict = {}


def mutability_and_identity():
    """可变性与对象标识 —— Python 内存模型"""

    print("\n" + "=" * 60)
    print("可变性与对象标识")
    print("=" * 60)

    # Python 中一切都是对象（类似 Java 的包装类型）
    # id() 相当于 System.identityHashCode()
    a = [1, 2, 3]
    b = a           # b 和 a 指向同一对象（Java 的引用赋值）
    c = a.copy()    # c 是浅拷贝（new ArrayList<>(a)）

    print(f"a is b: {a is b}")      # True（同一对象）
    print(f"a is c: {a is c}")      # False（不同对象）
    print(f"a == c: {a == c}")      # True（值相等）

    a.append(4)
    print(f"a: {a}, b: {b}, c: {c}")  # b 也变了，c 没变

    # 不可变类型：int, float, str, tuple, frozenset
    # 可变类型：list, dict, set

    # Java 面试经典: String 不可变 —— Python 也一样
    s = "hello"
    # s[0] = "H"  # TypeError!
    s = "Hello"    # 这是创建了新对象，不是修改


def type_conversion():
    """类型转换"""

    print("\n" + "=" * 60)
    print("类型转换")
    print("=" * 60)

    # Python 没有自动类型提升（不会 int -> float 隐式转换...除了算术运算）
    # 但算术运算中 int + float = float
    print(f"1 + 2.0 = {1 + 2.0}, type: {type(1 + 2.0)}")

    # 显式转换（类似 Java 的 Integer.parseInt()）
    print(f"int('42') = {int('42')}")
    print(f"float('3.14') = {float('3.14')}")
    print(f"str(42) = {str(42)}")
    print(f"bool(0) = {bool(0)}")       # False
    print(f"bool(1) = {bool(1)}")       # True
    print(f"bool('') = {bool('')}")     # False
    print(f"bool('a') = {bool('a')}")   # True

    # Python 的 truthy/falsy 比 Java 丰富
    # Falsy: None, False, 0, 0.0, '', [], {}, set()
    # Java 只有 boolean 可以做条件判断，Python 任何对象都可以
    if [1, 2, 3]:
        print("非空列表是 truthy")
    if not []:
        print("空列表是 falsy")


# =============================================================================
# 2. 变量与作用域
# =============================================================================

# 全局变量
GLOBAL_CONSTANT = "我是全局常量"  # Python 没有 final，用全大写约定表示常量

def scope_demo():
    """作用域 LEGB 规则"""

    print("\n" + "=" * 60)
    print("作用域 LEGB 规则")
    print("=" * 60)

    # Python 作用域: Local -> Enclosing -> Global -> Builtin
    # Java 作用域: 块级（{}）
    # 关键差异: Python 没有块级作用域！

    x = "local"

    # Java: for 循环内声明的变量，循环外访问不到
    # Python: for 循环内的变量，循环外仍然可以访问！
    for i in range(5):
        last = i
    print(f"循环外访问 i={i}, last={last}")  # 合法！Java 中不行

    # nonlocal 和 global 关键字
    counter = 0

    def increment():
        nonlocal counter    # 类似 Java 闭包中需要 AtomicInteger
        counter += 1

    increment()
    increment()
    print(f"counter = {counter}")  # 2


def unpacking_demo():
    """解构赋值 —— Java 没有的优雅特性"""

    print("\n" + "=" * 60)
    print("解构赋值")
    print("=" * 60)

    # 多重赋值
    a, b, c = 1, 2, 3
    print(f"a={a}, b={b}, c={c}")

    # 交换变量（Java 需要临时变量）
    a, b = b, a
    print(f"交换后: a={a}, b={b}")

    # 星号解构
    first, *rest = [1, 2, 3, 4, 5]
    print(f"first={first}, rest={rest}")

    *init, last = [1, 2, 3, 4, 5]
    print(f"init={init}, last={last}")

    # 嵌套解构
    (x, y), z = (1, 2), 3
    print(f"嵌套: x={x}, y={y}, z={z}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    basic_types()
    container_types()
    mutability_and_identity()
    type_conversion()
    scope_demo()
    unpacking_demo()
