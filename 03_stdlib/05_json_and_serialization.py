"""
Python3 JSON 与序列化 —— 写给 Java 开发者

核心概念：
- Python 内置 json 模块，无需第三方库
- 类比 Java: json 模块 ≈ Jackson/Gson，但更轻量
- pickle 是 Python 特有的二进制序列化，类似 Java Serializable
"""

import json
import pickle
import os
import tempfile
from dataclasses import dataclass, field, asdict, fields, is_dataclass
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


# =============================================================================
# 1. json.dumps / json.loads —— 对比 Java Jackson ObjectMapper
# =============================================================================

def json_basics_demo():
    """
    Java 对比:
    ObjectMapper mapper = new ObjectMapper();
    String s = mapper.writeValueAsString(obj);  // = json.dumps()
    Map m = mapper.readValue(s, Map.class);     // = json.loads()
    """
    print("=" * 60)
    print("1. json.dumps / json.loads 基本用法")
    print("=" * 60)

    user = {
        "name": "张三", "age": 30, "skills": ["Python", "Java"],
        "address": {"city": "北京", "zipcode": "100000"},
        "active": True, "score": None,  # None -> JSON null
    }

    # 序列化: Python 对象 -> JSON 字符串
    print(f"  默认: {json.dumps(user)[:60]}...")

    # 美化输出（类似 Jackson SerializationFeature.INDENT_OUTPUT）
    pretty = json.dumps(user, indent=2, ensure_ascii=False)
    print(f"  美化:\n{pretty}")

    # 反序列化: JSON 字符串 -> Python 对象
    parsed = json.loads(pretty)
    print(f"  loads: type={type(parsed).__name__}, name={parsed['name']}")
    # 类型映射: dict<->object, list<->array, str<->string,
    #           int/float<->number, True/False<->true/false, None<->null

    # sort_keys: 按键排序（方便 diff 比对）
    print(f"  sort_keys: {json.dumps(user, sort_keys=True, ensure_ascii=False)[:55]}...")


# =============================================================================
# 2. json.dump / json.load（文件操作）
# =============================================================================

def json_file_demo():
    """带 's' 的操作字符串，不带 's' 的操作文件"""
    print("\n" + "=" * 60)
    print("2. json.dump / json.load 文件操作")
    print("=" * 60)

    data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

    filepath = os.path.join(tempfile.gettempdir(), "demo_users.json")

    # 写入文件（Java: mapper.writeValue(new File(...), obj)）
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  已写入: {filepath}")

    # 从文件读取（Java: mapper.readValue(new File(...), Map.class)）
    with open(filepath, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"  读取结果: {loaded['users'][0]}")

    os.remove(filepath)


# =============================================================================
# 3. 自定义序列化 —— 对比 Java @JsonSerialize
# =============================================================================

def custom_serialization_demo():
    """处理 json 默认不支持的类型: datetime, Decimal, set, Enum"""
    print("\n" + "=" * 60)
    print("3. 自定义序列化（default 参数, JSONEncoder）")
    print("=" * 60)

    class Color(Enum):
        RED = "red"
        GREEN = "green"

    data = {
        "created": datetime(2024, 1, 15, 10, 30, 0),
        "amount": Decimal("99.95"),
        "tags": {"python", "json"},  # set 不支持
        "color": Color.RED,
    }

    # --- 方式一: default 参数（简单场景推荐）---
    def custom_default(obj):
        if isinstance(obj, datetime):  return obj.isoformat()
        if isinstance(obj, Decimal):   return float(obj)
        if isinstance(obj, set):       return sorted(list(obj))
        if isinstance(obj, Enum):      return obj.value
        raise TypeError(f"无法序列化: {type(obj)}")

    print("  --- default 参数 ---")
    print(json.dumps(data, default=custom_default, indent=2, ensure_ascii=False))

    # --- 方式二: 自定义 JSONEncoder（复杂场景，类似 Java JsonSerializer）---
    class EnhancedEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime, date)):  return obj.isoformat()
            if isinstance(obj, Decimal):  return str(obj)  # 字符串保留精度
            if isinstance(obj, set):      return sorted(list(obj))
            if isinstance(obj, Enum):     return obj.value
            return super().default(obj)

    print("  --- JSONEncoder 子类 ---")
    print(json.dumps(data, cls=EnhancedEncoder, indent=2, ensure_ascii=False))


# =============================================================================
# 4. 处理日期、Decimal 等特殊类型
# =============================================================================

def special_types_demo():
    print("\n" + "=" * 60)
    print("4. 处理日期、Decimal 等特殊类型")
    print("=" * 60)

    # --- 日期: isoformat() 序列化, fromisoformat() 反序列化 ---
    now = datetime(2024, 6, 15, 14, 30, 45)
    date_json = json.dumps({"ts": now.isoformat()})
    restored_dt = datetime.fromisoformat(json.loads(date_json)["ts"])
    print(f"  日期往返: {now} -> JSON -> {restored_dt}")

    # --- object_hook: 反序列化时自动转换（类似 Jackson Deserializer）---
    def datetime_hook(dct):
        for key, val in dct.items():
            if isinstance(val, str):
                try:    dct[key] = datetime.fromisoformat(val)
                except (ValueError, TypeError): pass
        return dct

    event = json.loads('{"name": "会议", "start": "2024-06-15T09:00:00"}',
                       object_hook=datetime_hook)
    print(f"  object_hook: start={event['start']} ({type(event['start']).__name__})")

    # --- Decimal: parse_float 避免精度丢失 ---
    print(f"  float 精度: 0.1+0.2 = {0.1 + 0.2}")
    price_json = '{"price": 19.99}'
    as_float = json.loads(price_json)["price"]
    as_decimal = json.loads(price_json, parse_float=Decimal)["price"]
    print(f"  默认float: {as_float} ({type(as_float).__name__})")
    print(f"  Decimal:   {as_decimal} ({type(as_decimal).__name__})")


# =============================================================================
# 5. pickle 模块 —— 对比 Java Serializable
# =============================================================================

# pickle 要求类定义在模块级别（类似 Java Serializable 需要 ClassLoader 可见）
class GameState:
    def __init__(self, player, level, inventory):
        self.player = player
        self.level = level
        self.inventory = inventory
        self.save_time = datetime.now()

    def __repr__(self):
        return f"GameState(player={self.player}, level={self.level})"


def pickle_demo():
    """
    pickle.dumps/loads ≈ Java ObjectOutputStream/ObjectInputStream
    只用于 Python 之间通信，不能跨语言！
    """
    print("\n" + "=" * 60)
    print("5. pickle 模块（类似 Java Serializable）")
    print("=" * 60)

    state = GameState("勇者", 42, ["圣剑", "盾牌", "药水"])

    # 序列化 / 反序列化
    pickled = pickle.dumps(state)
    restored = pickle.loads(pickled)
    print(f"  原始: {state}, inventory={state.inventory}")
    print(f"  还原: {restored}, inventory={restored.inventory}")
    print(f"  pickle 大小: {len(pickled)} bytes")

    # 文件操作: pickle.dump / pickle.load
    filepath = os.path.join(tempfile.gettempdir(), "game.pkl")
    with open(filepath, "wb") as f:
        pickle.dump(state, f)
    with open(filepath, "rb") as f:
        loaded = pickle.load(f)
    print(f"  文件往返: {loaded}")
    os.remove(filepath)

    # pickle vs json
    print("\n  pickle vs json:")
    print("  json:   文本可读 | 跨语言 | 仅基本类型 | 相对安全")
    print("  pickle: 二进制   | 仅Python | 任意对象  | 有安全风险")
    print("\n  [警告] 永远不要 unpickle 不信任的数据！可执行任意代码")


# =============================================================================
# 6. dataclass 与 JSON 的互转
# =============================================================================

@dataclass
class Address:
    city: str
    street: str
    zipcode: str = ""


@dataclass
class User:
    """Java 对比: @Data public class User { ... }  // Lombok"""
    name: str
    age: int
    email: str
    address: Address
    hobbies: list = field(default_factory=list)


def dataclass_json_demo():
    print("\n" + "=" * 60)
    print("6. dataclass 与 JSON 互转")
    print("=" * 60)

    # --- dataclass -> JSON: asdict() + json.dumps() ---
    user = User("李四", 28, "lisi@example.com",
                Address("上海", "南京路100号", "200000"), ["编程", "阅读"])
    print(f"  dataclass -> JSON:")
    print(json.dumps(asdict(user), indent=2, ensure_ascii=False))

    # --- JSON -> dataclass: 需要手动处理嵌套 ---
    json_str = ('{"name": "王五", "age": 35, "email": "ww@example.com", '
                '"address": {"city": "深圳", "street": "科技路1号"}, "hobbies": ["游泳"]}')
    raw = json.loads(json_str)
    addr = Address(**raw.pop("address"))
    restored = User(address=addr, **raw)
    print(f"  JSON -> dataclass: {restored}")

    # --- 通用递归转换辅助函数 ---
    def from_dict(cls, data: dict):
        """递归将 dict 转为 dataclass"""
        fieldtypes = {f.name: f.type for f in fields(cls)}
        kwargs = {}
        for key, value in data.items():
            ft = fieldtypes.get(key)
            if isinstance(value, dict) and isinstance(ft, type) and is_dataclass(ft):
                kwargs[key] = from_dict(ft, value)
            else:
                kwargs[key] = value
        return cls(**kwargs)

    user2 = from_dict(User, json.loads(json_str))
    print(f"  通用转换: {user2}")
    print(f"  类型验证: User={type(user2).__name__}, Address={type(user2.address).__name__}")


# =============================================================================
# 7. 常见陷阱和最佳实践
# =============================================================================

def pitfalls_and_best_practices_demo():
    print("\n" + "=" * 60)
    print("7. 常见陷阱和最佳实践")
    print("=" * 60)

    # 陷阱1: tuple 序列化后变成 list
    original = {"coords": (10, 20)}
    restored = json.loads(json.dumps(original))
    print(f"  陷阱1 tuple->list: {type(original['coords']).__name__} -> {type(restored['coords']).__name__}")

    # 陷阱2: int 键变成 str 键
    d = {1: "one", 2: "two"}
    restored = json.loads(json.dumps(d))
    print(f"  陷阱2 int键->str: {list(d.keys())} -> {list(restored.keys())}")

    # 陷阱3: 中文默认被转义
    msg = {"msg": "你好"}
    print(f"  陷阱3 ensure_ascii=True:  {json.dumps(msg)}")
    print(f"  陷阱3 ensure_ascii=False: {json.dumps(msg, ensure_ascii=False)}")

    # 陷阱4: NaN/Infinity 不是合法 JSON
    print(f"  陷阱4 NaN 默认允许: {json.dumps(float('nan'))}")
    try:
        json.dumps(float("nan"), allow_nan=False)
    except ValueError as e:
        print(f"  陷阱4 allow_nan=False: {e}")

    # 最佳实践
    print("\n  --- 最佳实践 ---")
    for p in [
        "1. ensure_ascii=False 处理中文",
        "2. indent 美化输出（调试时）",
        "3. parse_float=Decimal 处理金融数据",
        "4. 日期用 ISO 8601（isoformat）",
        "5. 不信任数据禁用 pickle",
        "6. 跨语言用 JSON，内部缓存可用 pickle",
        "7. dataclass + asdict() 是对象转 JSON 的首选",
    ]:
        print(f"  {p}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    json_basics_demo()
    json_file_demo()
    custom_serialization_demo()
    special_types_demo()
    pickle_demo()
    dataclass_json_demo()
    pitfalls_and_best_practices_demo()
