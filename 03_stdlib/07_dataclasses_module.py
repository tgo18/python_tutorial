"""
Python3 dataclasses —— 写给 Java 开发者

核心概念：
- dataclass 自动生成 __init__, __repr__, __eq__ 等样板代码
- 类比 Java: 最接近 Java 14+ Record 或 Lombok @Data
- Python 3.7+ 内置，不需要额外依赖
"""

from dataclasses import dataclass, field, asdict, astuple, FrozenInstanceError, InitVar
from typing import Optional
import sys


# =============================================================================
# 1. @dataclass 基础 —— 对比 Java Record / Lombok @Data
# =============================================================================

def basic_dataclass_demo():
    """@dataclass 自动生成样板代码"""

    print("=" * 60)
    print("@dataclass 基础")
    print("=" * 60)

    # Java: public record User(String name, int age, String email) {}
    # 或 Lombok: @Data public class User { ... }
    @dataclass
    class User:
        name: str
        age: int
        email: str

    u1 = User("张三", 30, "zhang@example.com")
    u2 = User("张三", 30, "zhang@example.com")
    print(f"  创建: {u1}")                      # 自动 __repr__
    print(f"  相等: u1 == u2 -> {u1 == u2}")    # 自动 __eq__
    print(f"  访问: u1.name = {u1.name}")


# =============================================================================
# 2. 字段默认值和 field() —— 对比 Java default values
# =============================================================================

def field_defaults_demo():
    """字段默认值与 field() 高级配置"""

    print("\n" + "=" * 60)
    print("字段默认值和 field()")
    print("=" * 60)

    # Java 对比: @Builder.Default private int port = 8080;  (Lombok)
    @dataclass
    class Config:
        host: str = "localhost"
        port: int = 8080
        debug: bool = False

    print(f"  默认: {Config()}")
    print(f"  自定义: {Config(host='0.0.0.0', port=3000, debug=True)}")

    # 可变默认值必须用 field(default_factory=...)
    @dataclass
    class Team:
        name: str
        members: list[str] = field(default_factory=list)   # 正确
        # members: list = []  # 错误! 所有实例会共享同一个列表

    t1, t2 = Team("后端组"), Team("前端组")
    t1.members.append("张三")
    t2.members.append("李四")
    print(f"  t1: {t1}")
    print(f"  t2: {t2} (互不影响)")

    # field() 的 repr/compare 控制
    @dataclass
    class Product:
        name: str
        price: float
        _internal_id: str = field(repr=False, compare=False)

    p1 = Product("Python书", 59.9, "INT-001")
    p2 = Product("Python书", 59.9, "INT-002")
    print(f"  repr 隐藏 id: {p1}")
    print(f"  忽略 id 比较: {p1 == p2}")  # True


# =============================================================================
# 3. frozen=True 不可变数据类 —— 对比 Java Record 的不可变性
# =============================================================================

def frozen_demo():
    """frozen=True 创建不可变数据类"""

    print("\n" + "=" * 60)
    print("frozen=True 不可变数据类")
    print("=" * 60)

    # Java Record 天然不可变，Python 需要 frozen=True
    @dataclass(frozen=True)
    class Point:
        x: float
        y: float

    p = Point(3.0, 4.0)
    print(f"  point: {p}, hash: {hash(p)}")
    try:
        p.x = 5.0
    except FrozenInstanceError:
        print(f"  修改失败: FrozenInstanceError")

    # frozen 实例可做 dict key 或放入 set
    points = {Point(0, 0), Point(1, 1), Point(0, 0)}
    print(f"  set 去重: {points}")


# =============================================================================
# 4. __post_init__ 后处理
# =============================================================================

def post_init_demo():
    """__post_init__ 在 __init__ 之后自动调用"""

    print("\n" + "=" * 60)
    print("__post_init__ 后处理")
    print("=" * 60)

    @dataclass
    class Rectangle:
        width: float
        height: float
        area: float = field(init=False)  # 不出现在 __init__ 参数中

        def __post_init__(self):
            if self.width <= 0 or self.height <= 0:
                raise ValueError("宽高必须大于0")
            self.area = self.width * self.height

    print(f"  矩形: {Rectangle(3, 4)}")
    try:
        Rectangle(-1, 5)
    except ValueError as e:
        print(f"  验证失败: {e}")

    # InitVar: 只用于初始化、不存为字段的参数
    @dataclass
    class UserProfile:
        username: str
        password_hash: str = field(init=False, repr=False)
        raw_password: InitVar[str]

        def __post_init__(self, raw_password: str):
            self.password_hash = f"hashed_{raw_password[::-1]}"

    profile = UserProfile("admin", raw_password="secret123")
    print(f"  profile: {profile}, hash={profile.password_hash}")


# =============================================================================
# 5. 继承
# =============================================================================

def inheritance_demo():
    """dataclass 继承"""

    print("\n" + "=" * 60)
    print("dataclass 继承")
    print("=" * 60)

    # 父类有默认值时，子类无默认值字段会报错 -> 都给默认值
    @dataclass
    class BaseEntity:
        id: Optional[int] = None
        created_at: str = "2025-01-01"

    @dataclass
    class UserEntity(BaseEntity):
        name: str = ""
        email: str = ""

    user = UserEntity(id=1, name="张三", email="zhang@test.com")
    print(f"  user: {user}")
    print(f"  isinstance(user, BaseEntity): {isinstance(user, BaseEntity)}")


# =============================================================================
# 6. dataclass vs namedtuple vs TypedDict
# =============================================================================

def comparison_demo():
    """三种轻量级数据结构对比"""

    print("\n" + "=" * 60)
    print("dataclass vs namedtuple vs TypedDict")
    print("=" * 60)

    @dataclass
    class DC_User:
        name: str
        age: int

    from collections import namedtuple
    NT_User = namedtuple("NT_User", ["name", "age"])

    from typing import TypedDict
    class TD_User(TypedDict):
        name: str
        age: int

    print(f"  dataclass:  {DC_User('张三', 30)}  | 可变=True")
    print(f"  namedtuple: {NT_User('张三', 30)}  | 可变=False")
    print(f"  TypedDict:  {{'name': '张三', 'age': 30}}  | 本质是 dict")
    print("\n  选择指南:")
    print("    dataclass  -> 需要方法、可变、完整类功能")
    print("    namedtuple -> 不可变、轻量、元组兼容")
    print("    TypedDict  -> dict/JSON 交互、API 响应类型")


# =============================================================================
# 7. slots=True (Python 3.10+) 内存优化
# =============================================================================

def slots_demo():
    """slots=True 减少内存占用"""

    print("\n" + "=" * 60)
    print("slots=True 内存优化 (Python 3.10+)")
    print("=" * 60)

    if sys.version_info < (3, 10):
        print("  需要 Python 3.10+，当前版本不支持")
        return

    # Java 对象默认固定字段; Python 默认用 __dict__（灵活但耗内存）
    @dataclass
    class RegularPoint:
        x: float
        y: float

    @dataclass(slots=True)
    class SlottedPoint:
        x: float
        y: float

    rp, sp = RegularPoint(1.0, 2.0), SlottedPoint(1.0, 2.0)
    print(f"  普通有 __dict__: {hasattr(rp, '__dict__')}")
    print(f"  slots 无 __dict__: {hasattr(sp, '__dict__')}")
    rp.z = 3.0  # 普通可以动态加属性
    try:
        sp.z = 3.0
    except AttributeError as e:
        print(f"  slots 不能动态加属性: {e}")
    print("  大量实例时 slots 节省约 30-40% 内存")


# =============================================================================
# 8. asdict / astuple 转换
# =============================================================================

def conversion_demo():
    """asdict 和 astuple 做数据转换"""

    print("\n" + "=" * 60)
    print("asdict / astuple 转换")
    print("=" * 60)

    @dataclass
    class Address:
        city: str
        street: str

    @dataclass
    class Employee:
        name: str
        age: int
        address: Address

    emp = Employee("张三", 30, Address("北京", "长安街"))
    d = asdict(emp)       # 递归转字典（方便 JSON 序列化）
    print(f"  asdict:  {d}")
    print(f"  astuple: {astuple(emp)}")

    import json
    print(f"  JSON: {json.dumps(d, ensure_ascii=False)}")
    restored = Employee(d["name"], d["age"], Address(**d["address"]))
    print(f"  还原一致: {emp == restored}")


# =============================================================================
# 9. 实际应用：DTO / VO 模式
# =============================================================================

def dto_vo_demo():
    """模拟 Java 中常见的 DTO/VO 模式"""

    print("\n" + "=" * 60)
    print("实际应用：DTO / VO 模式")
    print("=" * 60)

    @dataclass
    class CreateOrderRequest:
        """请求 DTO"""
        product_id: int
        quantity: int
        coupon_code: Optional[str] = None

    @dataclass(frozen=True)
    class OrderResponse:
        """响应 VO（不可变，类似 Java Record）"""
        order_id: int
        product_name: str
        total_price: float
        status: str

    @dataclass
    class OrderEntity:
        """领域实体"""
        id: Optional[int] = None
        product_id: int = 0
        product_name: str = ""
        quantity: int = 0
        unit_price: float = 0.0

        @property
        def total_price(self) -> float:
            return self.quantity * self.unit_price

        def to_response(self, status: str = "CREATED") -> OrderResponse:
            return OrderResponse(
                order_id=self.id or 0, product_name=self.product_name,
                total_price=self.total_price, status=status,
            )

    # 模拟流程: Request DTO -> Entity -> Response VO
    req = CreateOrderRequest(product_id=1001, quantity=2)
    entity = OrderEntity(id=1, product_id=req.product_id,
                         product_name="Python实战",
                         quantity=req.quantity, unit_price=49.9)
    resp = entity.to_response()
    print(f"  请求 DTO: {req}")
    print(f"  响应 VO:  {resp}")
    try:
        resp.status = "PAID"
    except FrozenInstanceError:
        print(f"  VO 不可变，无法修改 status")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    basic_dataclass_demo()
    field_defaults_demo()
    frozen_demo()
    post_init_demo()
    inheritance_demo()
    comparison_demo()
    slots_demo()
    conversion_demo()
    dto_vo_demo()
