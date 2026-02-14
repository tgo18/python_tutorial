"""
Python3 面向对象 —— 写给 Java 开发者

核心差异：
- Python 支持多继承（Java 只能单继承 + 多接口实现）
- Python 没有 interface 关键字（用 ABC 或 Protocol 替代）
- Python 没有 public/private/protected（用命名约定 _private, __mangle）
- Python 的"魔术方法"（__xx__）相当于 Java 的 Object 方法 + 运算符重载
"""


# =============================================================================
# 1. 类的基本定义
# =============================================================================

class User:
    """
    基本类定义。

    Java 对比:
    public class User {
        private String name;
        private int age;
        private static int count = 0;

        public User(String name, int age) { ... }
    }
    """

    # 类变量（Java 的 static 变量）
    count = 0

    def __init__(self, name: str, age: int):
        """构造方法（Java 的 Constructor）"""
        # 实例变量（Java 的成员变量）
        self.name = name      # public（Python 没有 public 关键字）
        self._email = None    # 约定 protected（单下划线）
        self.__id = id(self)  # 名称改写 private（双下划线）
        self.age = age
        User.count += 1       # 等价于 Java 的 User.count++

    def greet(self):
        """实例方法（Java 的普通方法）
        注意: self 相当于 Java 的 this，但必须显式声明
        """
        return f"你好，我是{self.name}，{self.age}岁"

    @classmethod
    def from_dict(cls, data: dict):
        """类方法（类似 Java 的 static 工厂方法）"""
        return cls(data["name"], data["age"])

    @staticmethod
    def validate_age(age: int) -> bool:
        """静态方法（和 Java 的 static 方法一样）"""
        return 0 < age < 150

    def __str__(self):
        """类似 Java 的 toString()"""
        return f"User(name={self.name}, age={self.age})"

    def __repr__(self):
        """开发调试用的字符串表示（Java 中通常也是 toString）"""
        return f"User(name='{self.name}', age={self.age})"

    def __eq__(self, other):
        """类似 Java 的 equals()"""
        if not isinstance(other, User):
            return NotImplemented
        return self.name == other.name and self.age == other.age

    def __hash__(self):
        """类似 Java 的 hashCode()"""
        return hash((self.name, self.age))


def basic_class_demo():
    print("=" * 60)
    print("基本类定义")
    print("=" * 60)

    u1 = User("张三", 30)
    u2 = User.from_dict({"name": "李四", "age": 25})

    print(f"str: {u1}")
    print(f"repr: {repr(u2)}")
    print(f"greet: {u1.greet()}")
    print(f"count: {User.count}")
    print(f"validate: {User.validate_age(25)}")
    print(f"eq: {u1 == User('张三', 30)}")


# =============================================================================
# 2. Property（Java 的 Getter/Setter）
# =============================================================================

class Temperature:
    """
    @property 相当于 Java 的 getter/setter，但更优雅

    Java:
    private double celsius;
    public double getCelsius() { return celsius; }
    public void setCelsius(double c) { this.celsius = c; }
    public double getFahrenheit() { return celsius * 9/5 + 32; }
    """

    def __init__(self, celsius: float = 0):
        self._celsius = celsius     # 内部存储

    @property
    def celsius(self) -> float:
        """getter"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        """setter（带验证）"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """计算属性（只读）"""
        return self._celsius * 9 / 5 + 32


def property_demo():
    print("\n" + "=" * 60)
    print("Property（getter/setter）")
    print("=" * 60)

    t = Temperature(100)
    print(f"摄氏: {t.celsius}°C")
    print(f"华氏: {t.fahrenheit}°F")

    t.celsius = 0
    print(f"修改后: {t.celsius}°C = {t.fahrenheit}°F")

    try:
        t.celsius = -300   # 触发验证
    except ValueError as e:
        print(f"验证失败: {e}")


# =============================================================================
# 3. 继承
# =============================================================================

class Animal:
    """基类"""

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError("子类必须实现 speak 方法")

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"


class Dog(Animal):
    """
    单继承。
    Java: public class Dog extends Animal { ... }
    """

    def speak(self) -> str:
        return f"{self.name}: 汪汪!"

    def fetch(self, item: str) -> str:
        return f"{self.name} 捡回了 {item}"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name}: 喵~"


# --- 多继承（Java 做不到的事）---

class Flyable:
    """行为混入（Mixin），类似 Java 的 interface + default method"""

    def fly(self) -> str:
        return f"{self.name} 在飞翔"


class Swimmable:
    def swim(self) -> str:
        return f"{self.name} 在游泳"


class Duck(Animal, Flyable, Swimmable):
    """多继承：鸭子会飞也会游"""

    def speak(self) -> str:
        return f"{self.name}: 嘎嘎!"


def inheritance_demo():
    print("\n" + "=" * 60)
    print("继承与多态")
    print("=" * 60)

    animals: list[Animal] = [Dog("旺财"), Cat("咪咪"), Duck("唐老鸭")]

    # 多态（和 Java 完全一样的概念）
    for animal in animals:
        print(f"  {animal} -> {animal.speak()}")

    # 多继承
    duck = Duck("唐老鸭")
    print(f"\n多继承能力:")
    print(f"  {duck.fly()}")
    print(f"  {duck.swim()}")

    # MRO（方法解析顺序）—— Java 没有这个概念
    # Python 使用 C3 线性化算法解决多继承的菱形问题
    print(f"\nMRO: {[c.__name__ for c in Duck.__mro__]}")

    # isinstance / issubclass（Java 的 instanceof）
    print(f"\nisinstance(duck, Animal): {isinstance(duck, Animal)}")
    print(f"isinstance(duck, Flyable): {isinstance(duck, Flyable)}")
    print(f"issubclass(Duck, Swimmable): {issubclass(Duck, Swimmable)}")


# =============================================================================
# 4. 抽象基类（ABC）—— Java 的 interface/abstract class
# =============================================================================

from abc import ABC, abstractmethod


class Repository(ABC):
    """
    抽象基类 —— 等价于 Java 的 interface 或 abstract class

    Java:
    public interface Repository<T> {
        T findById(long id);
        List<T> findAll();
        void save(T entity);
    }
    """

    @abstractmethod
    def find_by_id(self, id: int):
        """必须由子类实现"""
        ...

    @abstractmethod
    def find_all(self) -> list:
        ...

    @abstractmethod
    def save(self, entity) -> None:
        ...

    def count(self) -> int:
        """默认实现（Java 8+ 的 default method）"""
        return len(self.find_all())


class InMemoryRepository(Repository):
    """具体实现"""

    def __init__(self):
        self._store: dict[int, dict] = {}
        self._next_id = 1

    def find_by_id(self, id: int):
        return self._store.get(id)

    def find_all(self) -> list:
        return list(self._store.values())

    def save(self, entity) -> None:
        if "id" not in entity:
            entity["id"] = self._next_id
            self._next_id += 1
        self._store[entity["id"]] = entity


def abc_demo():
    print("\n" + "=" * 60)
    print("抽象基类 (ABC)")
    print("=" * 60)

    # repo = Repository()  # TypeError: Can't instantiate abstract class
    repo = InMemoryRepository()
    repo.save({"name": "张三"})
    repo.save({"name": "李四"})
    print(f"count: {repo.count()}")
    print(f"findAll: {repo.find_all()}")
    print(f"findById(1): {repo.find_by_id(1)}")


# =============================================================================
# 5. 魔术方法（Dunder Methods）—— 运算符重载
# =============================================================================

class Vector:
    """演示魔术方法 —— Java 不支持运算符重载（Kotlin 支持）"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        """v1 + v2"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """v1 - v2"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """v * 3"""
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self):
        """abs(v) 计算模长"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self):
        """if v: ... 判断是否为零向量"""
        return self.x != 0 or self.y != 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __len__(self):
        """len(v) 虽然不太合理，演示用"""
        return 2

    def __getitem__(self, index):
        """v[0], v[1] 下标访问"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"Vector index {index} out of range")

    def __iter__(self):
        """支持 for x in v: ..."""
        yield self.x
        yield self.y


def magic_methods_demo():
    print("\n" + "=" * 60)
    print("魔术方法（运算符重载）")
    print("=" * 60)

    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"|v1| = {abs(v1)}")
    print(f"v1[0] = {v1[0]}, v1[1] = {v1[1]}")
    print(f"解构: x, y = v1 -> ", end="")
    x, y = v1
    print(f"x={x}, y={y}")


# =============================================================================
# 6. 描述符（高级）—— Java 的字段拦截器
# =============================================================================

class Validated:
    """描述符：通用字段验证器"""

    def __init__(self, validator, error_msg):
        self.validator = validator
        self.error_msg = error_msg

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, f"_validated_{self.name}", None)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"{self.name}: {self.error_msg}")
        setattr(obj, f"_validated_{self.name}", value)


class Order:
    """使用描述符做字段验证"""
    quantity = Validated(lambda v: isinstance(v, int) and v > 0, "必须是正整数")
    price = Validated(lambda v: isinstance(v, (int, float)) and v > 0, "必须是正数")

    def __init__(self, product: str, quantity: int, price: float):
        self.product = product
        self.quantity = quantity    # 触发 Validated.__set__
        self.price = price

    @property
    def total(self):
        return self.quantity * self.price


def descriptor_demo():
    print("\n" + "=" * 60)
    print("描述符（字段验证）")
    print("=" * 60)

    order = Order("Python书", 3, 59.9)
    print(f"订单: {order.product}, 数量={order.quantity}, "
          f"单价={order.price}, 总价={order.total}")

    try:
        Order("坏订单", -1, 59.9)
    except ValueError as e:
        print(f"验证失败: {e}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    basic_class_demo()
    property_demo()
    inheritance_demo()
    abc_demo()
    magic_methods_demo()
    descriptor_demo()
