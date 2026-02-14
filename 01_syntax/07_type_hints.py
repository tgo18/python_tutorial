"""
Python3 类型提示 —— 写给 Java 开发者

核心概念：
- Python 3.5+ 引入类型提示，3.10+ 语法更简洁
- 类比 Java: Python 类型提示是"可选的"，不影响运行时
- 配合 mypy 静态检查，接近 Java 的编译期类型安全
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Any, Callable, Generic, Literal, Optional, Protocol,
    TypedDict, TypeVar, cast, overload, runtime_checkable,
)


# ============================================================
# 1. 基本类型注解
# ============================================================

def basic_type_hints_demo():
    """基本类型注解（对比 Java 原生类型）"""

    print("=" * 60)
    print("基本类型注解")
    print("=" * 60)

    # Java: int age = 30;  Python: 类型提示只是"建议"，不影响运行时
    age: int = 30
    name: str = "张三"
    height: float = 1.75
    is_active: bool = True
    print(f"  age={age}, name={name}, height={height}, active={is_active}")

    # 函数参数和返回值注解
    # Java: public String greet(String name, int times) { ... }
    def greet(name: str, times: int) -> str:
        return (f"Hello, {name}! " * times).strip()

    print(f"  greet: {greet('李四', 2)}")

    # 运行时不强制！Java 编译失败，Python 只是"建议"
    wrong: int = "这其实是字符串"  # type: ignore
    print(f"  运行时不报错: {wrong} (实际: {type(wrong).__name__})")
    print(f"  函数注解: {greet.__annotations__}")


# ============================================================
# 2. 容器类型
# ============================================================

def container_type_hints_demo():
    """容器类型注解（对比 Java 泛型 List<Integer>, Map<String, Integer>）"""

    print("\n" + "=" * 60)
    print("容器类型注解")
    print("=" * 60)

    # Python 3.9+ 直接用内置类型；之前需 from typing import List, Dict
    scores: list[int] = [90, 85, 92]              # Java: List<Integer>
    ages: dict[str, int] = {"张三": 30, "李四": 25}  # Java: Map<String, Integer>
    tags: set[str] = {"python", "java", "go"}      # Java: Set<String>
    point: tuple[float, float] = (3.14, 2.72)      # 固定长度 tuple
    data: tuple[int, ...] = (1, 2, 3, 4, 5)        # 可变长度 tuple
    print(f"  scores={scores}, ages={ages}")
    print(f"  tags={tags}, point={point}, data={data}")

    # 嵌套泛型（Java: Map<String, List<Integer>>）
    grades: dict[str, list[int]] = {"张三": [90, 85], "李四": [78, 88]}
    print(f"  嵌套: {grades}")

    def average(numbers: list[float]) -> float:
        return sum(numbers) / len(numbers) if numbers else 0.0
    print(f"  平均分: {average([90.0, 85.0, 92.0]):.1f}")


# ============================================================
# 3. Optional 和 Union
# ============================================================

def optional_union_demo():
    """Optional 和 Union（对比 Java Optional<String>）"""

    print("\n" + "=" * 60)
    print("Optional 和 Union")
    print("=" * 60)

    # Java: Optional<String> findUser(int id)
    # Python: Optional[str] 等价于 str | None（3.10+ 推荐 | 语法）
    def find_user(user_id: int) -> Optional[str]:
        return {1: "张三", 2: "李四"}.get(user_id)
    print(f"  find_user(1): {find_user(1)}, find_user(99): {find_user(99)}")

    # Union：多种类型之一（Java 没有直接对应，需 Object 或自定义接口）
    def parse_id(value: int | str) -> int:
        return int(value) if isinstance(value, str) else value
    print(f"  parse_id(42): {parse_id(42)}, parse_id('100'): {parse_id('100')}")

    # 类型收窄 / narrowing（mypy 在分支内推断类型）
    name: str | None = find_user(1)
    if name is not None:
        print(f"  类型收窄: {name.upper()}")  # mypy 知道此处是 str


# ============================================================
# 4. Callable 类型
# ============================================================

def callable_type_demo():
    """Callable 类型（对比 Java Function/Consumer/Supplier 接口）"""

    print("\n" + "=" * 60)
    print("Callable 类型")
    print("=" * 60)

    # Callable[[参数类型...], 返回类型]
    square: Callable[[int], int] = lambda x: x * x       # Function<Int,Int>
    printer: Callable[[str], None] = print                # Consumer<String>
    greeter: Callable[[], str] = lambda: "你好世界"         # Supplier<String>
    print(f"  square(5)={square(5)}, greeter()={greeter()}")

    # 高阶函数中使用 Callable
    def apply_all(items: list[int], func: Callable[[int], int]) -> list[int]:
        return [func(x) for x in items]
    nums = [1, 2, 3, 4, 5]
    print(f"  doubled: {apply_all(nums, lambda x: x * 2)}")
    print(f"  squared: {apply_all(nums, square)}")


# ============================================================
# 5. TypeVar 和泛型
# ============================================================

T = TypeVar("T")
N = TypeVar("N", int, float)  # 有界：限制为 int 或 float

def typevar_generic_demo():
    """TypeVar 和泛型（对比 Java <T>）"""

    print("\n" + "=" * 60)
    print("TypeVar 和泛型")
    print("=" * 60)

    # Java: public <T> T first(List<T> items) { return items.get(0); }
    def first(items: list[T]) -> T:
        return items[0]
    print(f"  first([10,20]): {first([10, 20])}, first(['a','b']): {first(['a', 'b'])}")

    # 有界 TypeVar（Java: <T extends Number>）
    def add_numbers(a: N, b: N) -> N:
        return a + b  # type: ignore
    print(f"  add(3,5)={add_numbers(3, 5)}, add(1.5,2.5)={add_numbers(1.5, 2.5)}")

    # 泛型类（Java: class Box<T> { T value; }）
    class Box(Generic[T]):
        def __init__(self, value: T) -> None:
            self.value = value
        def get(self) -> T:
            return self.value
        def __repr__(self) -> str:
            return f"Box({self.value!r})"
    print(f"  {Box(42)}.get()={Box(42).get()}, {Box('hi')}.get()={Box('hi').get()}")
    # Python 3.12+: def first[T](items: list[T]) -> T: ...  (PEP 695)


# ============================================================
# 6. Protocol（结构化子类型）
# ============================================================

def protocol_demo():
    """Protocol 结构化子类型（对比 Java interface）"""

    print("\n" + "=" * 60)
    print("Protocol（结构化子类型）")
    print("=" * 60)

    # Java 接口需要 implements；Python Protocol 只要"形状"匹配
    @runtime_checkable
    class Drawable(Protocol):
        def draw(self) -> str: ...

    class Circle:
        def draw(self) -> str: return "Circle: O"

    class Square:
        def draw(self) -> str: return "Square: []"

    class NotDrawable:
        def move(self) -> str: return "Moving..."

    def render(shape: Drawable) -> None:
        print(f"  {shape.draw()}")

    render(Circle())   # OK: 有 draw()
    render(Square())   # OK: 有 draw()
    # render(NotDrawable())  # mypy 报错：缺少 draw()

    print(f"  Circle 是 Drawable? {isinstance(Circle(), Drawable)}")
    print(f"  NotDrawable 是 Drawable? {isinstance(NotDrawable(), Drawable)}")
    print(f"  区别: Java 需 implements，Python 只看方法签名（鸭子类型）")


# ============================================================
# 7. TypedDict
# ============================================================

def typed_dict_demo():
    """TypedDict（对比 Java Map<String, Object> with specific keys）"""

    print("\n" + "=" * 60)
    print("TypedDict")
    print("=" * 60)

    # Java Map<String, Object> 丢失字段类型；TypedDict 给每个 key 指定类型
    class UserInfo(TypedDict):
        name: str
        age: int
        email: str

    user: UserInfo = {"name": "张三", "age": 30, "email": "z@test.com"}
    print(f"  user: {user}")
    print(f"  运行时类型: {type(user).__name__}")  # dict，不是 UserInfo

    class Config(TypedDict, total=False):  # total=False: 所有字段可选
        host: str
        port: int
    print(f"  partial: {Config(host='localhost')}")

    class ApiResponse(TypedDict):  # 适合标注 JSON API 响应
        status: int
        data: list[dict[str, Any]]
    resp: ApiResponse = {"status": 200, "data": [{"id": 1}]}
    print(f"  API: status={resp['status']}, data={resp['data']}")


# ============================================================
# 8. Literal 类型
# ============================================================

def literal_type_demo():
    """Literal 类型（限制参数为特定字面值）"""

    print("\n" + "=" * 60)
    print("Literal 类型")
    print("=" * 60)

    # Java 用枚举限制值；Python Literal 直接限制字面值
    def set_color(color: Literal["red", "green", "blue"]) -> str:
        return f"颜色: {color}"
    print(f"  {set_color('red')}, {set_color('blue')}")
    # set_color("yellow")  # mypy 报错

    # 结合 overload 让返回类型随参数变化
    @overload
    def parse(value: str, as_type: Literal["int"]) -> int: ...
    @overload
    def parse(value: str, as_type: Literal["float"]) -> float: ...
    def parse(value: str, as_type: str) -> int | float:
        return int(value) if as_type == "int" else float(value)

    print(f"  parse('42','int'): {parse('42', 'int')}")
    print(f"  parse('3.14','float'): {parse('3.14', 'float')}")


# ============================================================
# 9. dataclass 与类型提示的结合
# ============================================================

def dataclass_demo():
    """dataclass 与类型提示（对比 Java Record / Lombok @Data）"""

    print("\n" + "=" * 60)
    print("dataclass 与类型提示")
    print("=" * 60)

    # Java 16+: public record User(String name, int age) {}
    @dataclass
    class User:
        name: str
        age: int
        email: str = "unknown"
        tags: list[str] = field(default_factory=list)
        def is_adult(self) -> bool: return self.age >= 18

    u1, u2 = User("张三", 30, "z@test.com"), User("李四", 16)
    print(f"  u1: {u1}")
    print(f"  u2: {u2}")
    print(f"  is_adult: u1={u1.is_adult()}, u2={u2.is_adult()}")

    # 不可变 dataclass（类似 Java Record）
    @dataclass(frozen=True)
    class Point:
        x: float
        y: float
        def distance_to(self, other: Point) -> float:
            return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    p1, p2 = Point(0.0, 0.0), Point(3.0, 4.0)
    print(f"  距离 {p1} -> {p2}: {p1.distance_to(p2)}")

    try:
        p1.x = 10.0  # type: ignore
    except AttributeError as e:
        print(f"  frozen 不可变: {e}")

    pts = {Point(1.0, 2.0), Point(3.0, 4.0), Point(1.0, 2.0)}
    print(f"  Point set (去重): {pts}")


# ============================================================
# 10. mypy 简介和使用提示
# ============================================================

def mypy_tips_demo():
    """mypy 静态类型检查器简介"""

    print("\n" + "=" * 60)
    print("mypy 简介和使用提示")
    print("=" * 60)

    print("""  安装: pip install mypy
  使用: mypy script.py / mypy --strict src/
  配置 (pyproject.toml):
    [tool.mypy]
    python_version = "3.10"
    disallow_untyped_defs = true
  指令: # type: ignore (忽略), cast() (强转)""")

    # cast 示例（类似 Java 强转 (String) obj）
    data: Any = "hello"
    print(f"  cast 示例: {cast(str, data).upper()}")

    # 渐进式类型检查
    def legacy(x, y):  # type: ignore[no-untyped-def]
        return x + y  # 旧代码暂无注解

    def typed(x: int, y: int) -> int:
        return x + y  # 新代码有完整注解

    print(f"  legacy(1,2)={legacy(1, 2)}, typed(1,2)={typed(1, 2)}")

    # Java vs Python 对比总结
    rows = [
        ("类型检查时机", "编译期（强制）", "mypy 静态分析（可选）"),
        ("运行时类型",  "擦除泛型",      "完全忽略注解"),
        ("空安全",     "@Nullable",    "Optional / X | None"),
        ("泛型",      "<T extends F>", "TypeVar + bound"),
        ("接口",      "interface",     "Protocol（结构化）"),
        ("严格程度",   "始终严格",       "可配置（渐进式）"),
    ]
    print(f"\n  {'对比项':<14} {'Java':<20} {'Python + mypy'}")
    print(f"  {'-' * 54}")
    for item, java, python in rows:
        print(f"  {item:<14} {java:<20} {python}")


# ============================================================
# 运行所有 demo
# ============================================================

if __name__ == "__main__":
    basic_type_hints_demo()
    container_type_hints_demo()
    optional_union_demo()
    callable_type_demo()
    typevar_generic_demo()
    protocol_demo()
    typed_dict_demo()
    literal_type_demo()
    dataclass_demo()
    mypy_tips_demo()
