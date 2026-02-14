"""
Python3 collections 模块 —— 写给 Java 开发者

核心概念：
- collections 提供了比内置 dict/list/set 更强大的容器类型
- 类比 Java: java.util.Collections 工具类 + Guava 增强容器
"""

from collections import namedtuple, deque, Counter, defaultdict, OrderedDict, ChainMap


# =============================================================================
# 1. namedtuple —— 对比 Java Record / Lombok @Value
# =============================================================================

def namedtuple_demo():
    """namedtuple: 带字段名的不可变元组"""

    print("=" * 60)
    print("1. namedtuple —— 对比 Java Record / Lombok @Value")
    print("=" * 60)

    # Java:  public record Point(int x, int y) {}
    #        Point p = new Point(3, 4);  p.x();  // 3
    # Python namedtuple —— 一行搞定不可变数据类
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)

    print(f"点: {p}")                       # Point(x=3, y=4)
    print(f"x={p.x}, y={p.y}")             # 用属性名访问（Java 的 p.x()）
    print(f"索引访问: p[0]={p[0]}")         # 也支持索引（tuple 特性）

    # 不可变性 —— 和 Java Record 一样
    # p.x = 10  # AttributeError! 不可变

    # 解构赋值 —— Java Record 做不到
    x, y = p
    print(f"解构: x={x}, y={y}")

    # --- 字段声明: 列表 / 逗号字符串 / 空格字符串 ---
    Color = namedtuple("Color", ["red", "green", "blue"])
    print(f"\n颜色: {Color(255, 128, 0)}")

    # --- 默认值 ---
    User = namedtuple("User", ["name", "age", "email"], defaults=["unknown@test.com"])
    u1 = User("张三", 30)                   # email 使用默认值
    print(f"用户: {u1}")

    # --- 实用方法 ---
    print(f"转字典: {u1._asdict()}")                        # Java Record 没有
    print(f"替换: {u1._replace(age=31)}")                   # 类似 Lombok @With
    print(f"字段名: {User._fields}")
    print(f"从字典创建: {User(**{'name': '王五', 'age': 28, 'email': 'ww@test.com'})}")


# =============================================================================
# 2. deque —— 对比 Java ArrayDeque
# =============================================================================

def deque_demo():
    """deque: 双端队列，两端操作 O(1)"""

    print("\n" + "=" * 60)
    print("2. deque —— 对比 Java ArrayDeque")
    print("=" * 60)

    # Java:  Deque<String> dq = new ArrayDeque<>();
    # Python list.insert(0, x) 是 O(n)，deque.appendleft 是 O(1)
    dq = deque(["b", "c", "d"])

    # --- 两端操作 ---
    dq.appendleft("a")             # Java: addFirst("a")
    dq.append("e")                 # Java: addLast("e")
    print(f"两端添加后: {dq}")

    left = dq.popleft()            # Java: pollFirst()
    right = dq.pop()               # Java: pollLast()
    print(f"弹出 left={left}, right={right}, 剩余: {dq}")

    # --- 旋转（Java ArrayDeque 没有）---
    dq_rotate = deque([1, 2, 3, 4, 5])
    dq_rotate.rotate(2)            # 右旋 2 步: [4, 5, 1, 2, 3]
    print(f"右旋 2 步: {dq_rotate}")

    # --- maxlen: 固定长度队列（滑动窗口）---
    # Java 中需要手动维护或用 Guava EvictingQueue
    recent = deque(maxlen=3)
    for log in ["登录", "查询", "修改", "退出"]:
        recent.append(log)
        print(f"  滑动窗口: {list(recent)}")

    # --- 用 deque 实现栈和队列 ---
    stack = deque()                     # 栈 (LIFO): append + pop
    stack.append("A"); stack.append("B"); stack.append("C")
    print(f"\n栈弹出: {stack.pop()}")   # C

    queue = deque()                     # 队列 (FIFO): append + popleft
    queue.append("A"); queue.append("B"); queue.append("C")
    print(f"队列取出: {queue.popleft()}")  # A


# =============================================================================
# 3. Counter —— 对比 Java 手动 Map 计数
# =============================================================================

def counter_demo():
    """Counter: 计数器，统计元素出现次数"""

    print("\n" + "=" * 60)
    print("3. Counter —— 对比 Java 手动 Map 计数")
    print("=" * 60)

    # Java:  Map<Character, Integer> counts = new HashMap<>();
    #        for (char c : s.toCharArray()) counts.merge(c, 1, Integer::sum);
    # Python 一行搞定:
    counter = Counter("abracadabra")
    print(f"字符计数: {counter}")
    print(f"最常见 3 个: {counter.most_common(3)}")
    print(f"'a' 出现: {counter['a']}, 'z' 出现: {counter['z']}")  # 不存在返回 0

    # --- Counter 算术运算（Java 需大量手动代码）---
    c1, c2 = Counter(a=3, b=1), Counter(a=1, b=2)
    print(f"\nc1 + c2 = {c1 + c2}")     # 合并: Counter({{'a': 4, 'b': 3}})
    print(f"c1 - c2 = {c1 - c2}")       # 差集（只保留正数）
    print(f"c1 & c2 = {c1 & c2}")       # 交集（取最小值）
    print(f"c1 | c2 = {c1 | c2}")       # 并集（取最大值）

    # --- 实战：统计日志级别 ---
    logs = ["INFO", "ERROR", "INFO", "WARN", "INFO", "ERROR",
            "DEBUG", "INFO", "WARN", "ERROR"]
    log_stats = Counter(logs)
    print(f"\n日志级别统计:")
    for level, count in log_stats.most_common():
        print(f"  {level:>5}: {'#' * count} ({count})")

    # --- update / subtract ---
    c = Counter(a=4, b=2)
    c.update({"a": 1, "c": 3})         # 增加计数
    print(f"\nupdate 后: {c}")
    c.subtract({"a": 2, "b": 1})       # 减少计数（允许负数）
    print(f"subtract 后: {c}")


# =============================================================================
# 4. defaultdict —— 对比 Java getOrDefault / computeIfAbsent
# =============================================================================

def defaultdict_demo():
    """defaultdict: 带默认值的字典"""

    print("\n" + "=" * 60)
    print("4. defaultdict —— 对比 Java getOrDefault / computeIfAbsent")
    print("=" * 60)

    # Java:  groups.computeIfAbsent("fruits", k -> new ArrayList<>()).add("apple");

    # --- 分组（最常见用法，自动初始化默认值）---
    groups = defaultdict(list)          # 默认值为空列表
    items = [("水果", "苹果"), ("蔬菜", "白菜"), ("水果", "香蕉"),
             ("蔬菜", "萝卜"), ("水果", "橘子"), ("肉类", "牛肉")]

    for category, item in items:
        groups[category].append(item)   # 无需检查 key 是否存在！

    print("分组结果:")
    for k, v in groups.items():
        print(f"  {k}: {v}")

    # --- 计数（Counter 更专业，但 defaultdict(int) 也能做）---
    word_count = defaultdict(int)       # 默认值为 0
    for word in "hello world hello python hello world".split():
        word_count[word] += 1           # Java: map.merge(word, 1, Integer::sum)
    print(f"\n单词计数: {dict(word_count)}")

    # --- 集合去重分组 ---
    tags = defaultdict(set)
    for user, skill in [("用户A", "Python"), ("用户A", "Java"),
                         ("用户B", "Python"), ("用户A", "Python"), ("用户B", "Go")]:
        tags[user].add(skill)           # set 自动去重
    print(f"\n技能标签: { {u: s for u, s in tags.items()} }")

    # --- 嵌套 defaultdict ---
    # Java: Map<String, Map<String, Integer>> 初始化很痛苦
    matrix = defaultdict(lambda: defaultdict(int))
    matrix["row1"]["col1"] = 10
    matrix["row1"]["col2"] = 20
    print(f"\n嵌套: matrix['row1']['col2'] = {matrix['row1']['col2']}")
    print(f"不存在的键: matrix['row9']['col9'] = {matrix['row9']['col9']}")  # 0

    # --- 与普通 dict 的对比: 普通 dict 访问不存在的键抛 KeyError ---
    dd = defaultdict(str)               # 默认值为空字符串
    print(f"\ndefaultdict 自动返回默认值: '{dd['missing']}'")  # 不抛异常


# =============================================================================
# 5. OrderedDict —— 对比 Java LinkedHashMap
# =============================================================================

def ordereddict_demo():
    """OrderedDict: 记住插入顺序的字典"""

    print("\n" + "=" * 60)
    print("5. OrderedDict —— 对比 Java LinkedHashMap")
    print("=" * 60)

    # Python 3.7+ 普通 dict 也保证插入顺序，但 OrderedDict 仍有独特价值
    # Java:  Map<String, Integer> map = new LinkedHashMap<>();
    od = OrderedDict()
    od["banana"] = 2; od["apple"] = 1; od["cherry"] = 3
    print(f"OrderedDict: {od}")

    # --- 特有功能 1: move_to_end ---
    od.move_to_end("banana")                    # 移到末尾
    print(f"banana 移末尾: {od}")
    od.move_to_end("cherry", last=False)        # 移到开头
    print(f"cherry 移开头: {od}")

    # --- 特有功能 2: popitem 可从两端弹出 ---
    od2 = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
    last = od2.popitem(last=True)               # 弹末尾
    first = od2.popitem(last=False)             # 弹开头
    print(f"\n弹末尾: {last}, 弹开头: {first}, 剩余: {od2}")

    # --- 特有功能 3: 相等性比较考虑顺序 ---
    d1, d2 = {"a": 1, "b": 2}, {"b": 2, "a": 1}
    print(f"\n普通 dict 比较: {d1 == d2}")       # True（只看内容）

    od1 = OrderedDict([("a", 1), ("b", 2)])
    od2 = OrderedDict([("b", 2), ("a", 1)])
    print(f"OrderedDict 比较: {od1 == od2}")     # False!（顺序不同）

    # --- 实战: LRU 缓存（Java LinkedHashMap 重写 removeEldestEntry）---
    class SimpleLRU:
        def __init__(self, capacity):
            self.capacity = capacity
            self.cache = OrderedDict()

        def get(self, key):
            if key in self.cache:
                self.cache.move_to_end(key)     # 标记为最近使用
                return self.cache[key]
            return -1

        def put(self, key, value):
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)   # 淘汰最久未使用

    lru = SimpleLRU(3)
    for k, v in [("a", 1), ("b", 2), ("c", 3)]:
        lru.put(k, v)
    print(f"\nLRU 缓存: {dict(lru.cache)}")

    lru.get("a")                # 访问 a，变为最近使用
    lru.put("d", 4)             # 容量满，淘汰最久未用的 b
    print(f"访问 a 后添加 d: {dict(lru.cache)}")
    print(f"b 已被淘汰: lru.get('b') = {lru.get('b')}")


# =============================================================================
# 6. ChainMap —— 多字典链式查找
# =============================================================================

def chainmap_demo():
    """ChainMap: 将多个字典串成链，按优先级查找"""

    print("\n" + "=" * 60)
    print("6. ChainMap —— 多字典链式查找")
    print("=" * 60)

    # Java 没有直接对应物（最接近: Spring PropertySource 链）

    # --- 基本用法: 配置覆盖（命令行 > 环境 > 默认）---
    defaults = {"color": "blue", "font_size": 12, "debug": False}
    env_config = {"color": "green", "log_level": "INFO"}
    cli_args = {"debug": True}

    config = ChainMap(cli_args, env_config, defaults)

    print("配置优先级链: cli_args > env_config > defaults")
    print(f"  color = {config['color']}")           # green（env 覆盖 default）
    print(f"  font_size = {config['font_size']}")   # 12（只在 default 中）
    print(f"  debug = {config['debug']}")           # True（cli 覆盖 default）

    # --- 修改只影响第一个字典 ---
    config["theme"] = "dark"
    print(f"\n写入后 cli_args = {cli_args}")        # 多了 theme

    # --- new_child: 添加更高优先级层（不改原链）---
    override = {"color": "red", "font_size": 16}
    new_config = config.new_child(override)
    print(f"\nnew_child 后 color = {new_config['color']}")  # red
    print(f"原 config 不变 color = {config['color']}")      # green

    # --- parents: 去掉第一层 ---
    parent_config = new_config.parents
    print(f"parents 后 color = {parent_config['color']}")   # green

    # --- 实战: 模拟作用域链（类似 LEGB 规则）---
    builtin_scope = {"print": "<built-in>", "len": "<built-in>"}
    global_scope = {"my_func": "<function>", "PI": 3.14159}
    local_scope = {"x": 42, "y": 100}

    scope = ChainMap(local_scope, global_scope, builtin_scope)
    print(f"\n模拟作用域链:")
    print(f"  x = {scope['x']}")                    # local
    print(f"  PI = {scope['PI']}")                   # global
    print(f"  print = {scope['print']}")             # builtin

    # 局部变量 "遮蔽" 全局变量
    local_scope["PI"] = 3.14
    print(f"  遮蔽后 PI = {scope['PI']}")           # 3.14（局部优先）


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    namedtuple_demo()
    deque_demo()
    counter_demo()
    defaultdict_demo()
    ordereddict_demo()
    chainmap_demo()
