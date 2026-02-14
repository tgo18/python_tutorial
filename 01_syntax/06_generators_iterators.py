"""
Python3 生成器与迭代器 —— 写给 Java 开发者

核心概念：
- 迭代器是实现了 __iter__ + __next__ 的对象（惰性求值）
- 生成器是用 yield 创建迭代器的语法糖（写起来极其简洁）
- 类比 Java: Iterator<T> 接口, Stream.generate(), Stream.iterate()
- 关键优势：内存效率极高，处理无限序列和大数据集的利器
"""

import sys
import itertools


# =============================================================================
# 1. 迭代器协议（__iter__ + __next__）
# =============================================================================

class RangeIterator:
    """
    手动实现迭代器。
    Java 对比:
    public class RangeIterator implements Iterator<Integer> {
        public boolean hasNext() { return current < end; }
        public Integer next() { return current++; }
    }
    Python 区别：没有 hasNext()，结束时抛出 StopIteration
    """

    def __init__(self, start: int, end: int):
        self.current = start
        self.end = end

    def __iter__(self):
        """返回迭代器自身（Java 的 Iterable.iterator()）"""
        return self

    def __next__(self):
        """返回下一个值，结束时抛 StopIteration"""
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


def iterator_protocol_demo():
    print("=" * 60)
    print("1. 迭代器协议（__iter__ + __next__）")
    print("=" * 60)

    # 手动迭代（Java 风格: while(iter.hasNext()) { iter.next(); }）
    it = RangeIterator(0, 5)
    print("  手动迭代:", end=" ")
    while True:
        try:
            print(next(it), end=" ")
        except StopIteration:
            break
    print()

    # for 循环自动处理 StopIteration（推荐写法）
    print(f"  for 循环: {list(RangeIterator(0, 5))}")

    # 迭代器是一次性的（消费后就空了）
    it = RangeIterator(0, 3)
    print(f"  第一次消费: {list(it)}")
    print(f"  第二次消费: {list(it)}")  # 空的！


# =============================================================================
# 2. 生成器函数（yield）
# =============================================================================

def my_range(start, end, step=1):
    """
    用 yield 重写 RangeIterator —— 代码量减少 80%
    Java 对比: Stream.iterate(start, n -> n < end, n -> n + step)
    """
    current = start
    while current < end:
        yield current       # 暂停并返回值
        current += step     # 下次 next() 从这里继续


def fibonacci():
    """无限斐波那契生成器 —— Java 的 Stream.generate() 需要额外状态管理"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def generator_function_demo():
    print("\n" + "=" * 60)
    print("2. 生成器函数（yield）")
    print("=" * 60)

    print(f"  my_range(0, 10, 2): {list(my_range(0, 10, 2))}")

    # 生成器是惰性的 —— 不调用 next() 就不执行
    gen = my_range(0, 3)
    print(f"  type: {type(gen)}")
    print(f"  逐个取值: {next(gen)}, {next(gen)}, {next(gen)}")

    # 无限序列 —— 用 islice 取前 10 个斐波那契数
    fib_10 = list(itertools.islice(fibonacci(), 10))
    print(f"  前 10 个斐波那契数: {fib_10}")


# =============================================================================
# 3. yield from 委托
# =============================================================================

def flatten(nested_list):
    """
    yield from 委托给子迭代器（还能透传 send/throw）
    等价于: for item in sub_iterable: yield item
    """
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)  # 递归展平
        else:
            yield item


def chain(*iterables):
    """模拟 itertools.chain"""
    for it in iterables:
        yield from it


def yield_from_demo():
    print("\n" + "=" * 60)
    print("3. yield from 委托")
    print("=" * 60)

    nested = [1, [2, 3], [4, [5, 6]], 7]
    print(f"  嵌套: {nested}")
    print(f"  展平: {list(flatten(nested))}")

    result = list(chain([1, 2], "AB", range(3)))
    print(f"  chain([1,2], 'AB', range(3)): {result}")


# =============================================================================
# 4. 生成器表达式 vs 列表推导（内存对比）
# =============================================================================

def memory_comparison_demo():
    print("\n" + "=" * 60)
    print("4. 生成器表达式 vs 列表推导（内存对比）")
    print("=" * 60)

    # 列表推导：立即创建，占用大量内存
    # Java: list.stream().map(x -> x*x).collect(Collectors.toList())
    squares_list = [x * x for x in range(100_000)]

    # 生成器表达式：惰性求值，几乎不占内存
    # Java: IntStream.range(0, 100000).map(x -> x*x)
    squares_gen = (x * x for x in range(100_000))

    list_size = sys.getsizeof(squares_list)
    gen_size = sys.getsizeof(squares_gen)
    print(f"  列表推导 size:   {list_size:>10,} bytes")
    print(f"  生成器表达式 size: {gen_size:>6,} bytes")
    print(f"  内存节省: {list_size // gen_size} 倍")

    # 语法区别：[] vs ()
    print(f"\n  [x*2 for x in range(5)] = {[x*2 for x in range(5)]}")
    print(f"  (x*2 for x in range(5)) = {(x*2 for x in range(5))}")

    # 生成器表达式直接传给函数（省括号）
    print(f"  sum(x*x for x in range(10)) = {sum(x * x for x in range(10))}")

    # 选择原则：多次遍历/索引 -> 列表；单次遍历/大数据 -> 生成器


# =============================================================================
# 5. send() / throw() / close() 高级用法
# =============================================================================

def accumulator():
    """
    协程式生成器 —— send() 向生成器发送数据
    Java 没有对应概念，可类比"可交互的状态机"
    """
    total = 0
    while True:
        value = yield total  # yield 返回 total，同时接收 send() 的值
        if value is None:
            break
        total += value


def send_throw_close_demo():
    print("\n" + "=" * 60)
    print("5. send() / throw() / close() 高级用法")
    print("=" * 60)

    # --- send(): 向生成器内部发送数据 ---
    print("  --- send() 累加器 ---")
    acc = accumulator()
    next(acc)                   # 必须先 next() 初始化，推进到第一个 yield
    print(f"    send(10): {acc.send(10)}")   # total = 10
    print(f"    send(20): {acc.send(20)}")   # total = 30
    print(f"    send(5):  {acc.send(5)}")    # total = 35

    # --- throw(): 向生成器抛异常 ---
    print("\n  --- throw() ---")

    def guarded_gen():
        try:
            while True:
                value = yield
                print(f"    收到: {value}")
        except ValueError as e:
            print(f"    捕获异常: {e}")
            yield "已恢复"

    g = guarded_gen()
    next(g)
    g.send("hello")
    result = g.throw(ValueError, "出错了")
    print(f"    throw 后返回: {result}")

    # --- close(): 优雅关闭，触发 GeneratorExit ---
    print("\n  --- close() ---")

    def resource_gen():
        print("    打开资源...")
        try:
            while True:
                yield "数据"
        except GeneratorExit:
            print("    关闭资源（GeneratorExit）")

    rg = resource_gen()
    next(rg)
    rg.close()


# =============================================================================
# 6. 实际应用：大文件、无限序列、管道处理
# =============================================================================

def read_large_file(filepath, chunk_size=64):
    """逐块读取大文件（Java: BufferedReader.lines()）"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except FileNotFoundError:
        yield f"[文件不存在: {filepath}]"


def infinite_id_generator(prefix="ID"):
    """无限 ID 生成器"""
    n = 0
    while True:
        n += 1
        yield f"{prefix}-{n:06d}"

# 管道处理函数（Unix pipe 风格）
def pipe_strip(source):
    for s in source: yield s.strip()

def pipe_nonempty(source):
    for s in source:
        if s: yield s

def pipe_lower(source):
    for s in source: yield s.lower()


def practical_demo():
    print("\n" + "=" * 60)
    print("6. 实际应用：大文件、无限序列、管道处理")
    print("=" * 60)

    # --- 读取大文件 ---
    print("  --- 逐块读取文件 ---")
    import os
    self_path = os.path.abspath(__file__)
    for i, chunk in enumerate(read_large_file(self_path, chunk_size=40)):
        if i >= 2:
            break
        print(f"    chunk {i}: {chunk!r}")

    # --- 无限 ID 生成器 ---
    print("\n  --- 无限 ID 生成器 ---")
    id_gen = infinite_id_generator("USR")
    print(f"    {[next(id_gen) for _ in range(4)]}")

    # --- 管道处理 ---
    # Java 对比: stream.map(String::trim).filter(s -> !s.isEmpty()).map(String::toLowerCase)
    print("\n  --- 管道处理 ---")
    raw = ["  Hello World  ", "  PYTHON  ", "", "  Generator  "]
    pipeline = pipe_lower(pipe_nonempty(pipe_strip(iter(raw))))
    print(f"    原始数据: {raw}")
    print(f"    管道结果: {list(pipeline)}")
    # 所有阶段惰性求值，数据逐条流过管道，内存使用恒定


# =============================================================================
# 7. itertools 简要介绍（预告第三章）
# =============================================================================

def itertools_preview_demo():
    print("\n" + "=" * 60)
    print("7. itertools 简要介绍（预告第三章详解）")
    print("=" * 60)

    # count / cycle：无限迭代器
    counter = itertools.count(start=1, step=2)
    print(f"  count(1,2) 前5个: {[next(counter) for _ in range(5)]}")
    colors = itertools.cycle(["红", "绿", "蓝"])
    print(f"  cycle 前6个: {[next(colors) for _ in range(6)]}")

    # chain / islice
    print(f"  chain: {list(itertools.chain([1, 2], [3, 4], [5]))}")
    print(f"  islice(fib, 8): {list(itertools.islice(fibonacci(), 8))}")

    # takewhile / dropwhile（类似 Java Stream.takeWhile / dropWhile）
    nums = [1, 3, 5, 2, 4, 6]
    print(f"  takewhile(<4, {nums}): {list(itertools.takewhile(lambda x: x < 4, nums))}")
    print(f"  dropwhile(<4, {nums}): {list(itertools.dropwhile(lambda x: x < 4, nums))}")

    # groupby（需要先排序！类似 Collectors.groupingBy）
    data = sorted([("A", 1), ("B", 3), ("A", 2), ("B", 4)], key=lambda x: x[0])
    groups = {k: list(v) for k, v in itertools.groupby(data, key=lambda x: x[0])}
    print(f"  groupby: {groups}")

    # 排列组合
    print(f"  product('AB','12'): {list(itertools.product('AB', '12'))}")
    print(f"  combinations('ABCD',2): {list(itertools.combinations('ABCD', 2))}")

    print("\n  (更多 itertools 将在第三章标准库中详解)")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    iterator_protocol_demo()
    generator_function_demo()
    yield_from_demo()
    memory_comparison_demo()
    send_throw_close_demo()
    practical_demo()
    itertools_preview_demo()
