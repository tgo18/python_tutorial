"""
Python3 上下文管理器 —— 写给 Java 开发者

核心概念：
- with 语句确保资源被正确释放，类似 Java 的 try-with-resources
- 类比 Java: __enter__/__exit__ ≈ AutoCloseable.close()
- contextlib 提供了更便捷的上下文管理器创建方式
"""

import contextlib
import io
import os
import tempfile
import time


# =============================================================================
# 1. with 语句基础 —— 对比 Java try-with-resources
# =============================================================================

def with_basics_demo():
    """with 语句基础用法"""
    print("=" * 60)
    print("1. with 语句基础（对比 Java try-with-resources）")
    print("=" * 60)

    # Java: try (BufferedReader br = new BufferedReader(...)) { ... }
    # Python: with open(...) as f: ...
    tmp_path = os.path.join(tempfile.gettempdir(), "_ctx_demo.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write("Hello, Context Manager!\n")

    with open(tmp_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  文件内容: {content.strip()}")
    print(f"  文件已关闭? {f.closed}")  # True

    # 同时管理多个资源
    with open(tmp_path, "r") as src, open(os.devnull, "w") as dst:
        dst.write(src.read())
    print(f"  多资源同时关闭: src={src.closed}, dst={dst.closed}")
    os.remove(tmp_path)

    # with 等价于 try-finally
    # f = open(path)
    # try:     data = f.read()
    # finally: f.close()


# =============================================================================
# 2. __enter__ / __exit__ 协议 —— 对比 Java AutoCloseable
# =============================================================================

class ManagedResource:
    """
    Java 对比: implements AutoCloseable { void close(); }
    Python 的 __exit__ 更强大：能接收异常信息并决定是否吞掉
    """

    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        """进入 with 块时调用，返回值赋给 as 变量"""
        print(f"  [enter] 打开: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开 with 块时调用（无论是否异常）
        返回 True 吞掉异常，False 继续传播"""
        if exc_type:
            print(f"  [exit]  异常: {exc_type.__name__}: {exc_val}")
        print(f"  [exit]  关闭: {self.name}")
        return False

    def do_work(self, fail=False):
        if fail:
            raise RuntimeError(f"{self.name} 出错!")
        return f"{self.name}: 完成"


def enter_exit_demo():
    """__enter__ / __exit__ 协议演示"""
    print("\n" + "=" * 60)
    print("2. __enter__/__exit__ 协议（对比 Java AutoCloseable）")
    print("=" * 60)

    print("--- 正常 ---")
    with ManagedResource("DB连接") as res:
        print(f"  {res.do_work()}")

    # 异常——__exit__ 仍然被调用
    print("\n--- 异常（资源仍被清理）---")
    try:
        with ManagedResource("文件句柄") as res:
            res.do_work(fail=True)
    except RuntimeError as e:
        print(f"  外部捕获: {e}")


# =============================================================================
# 3. contextlib.contextmanager 装饰器（yield 方式）
# =============================================================================

@contextlib.contextmanager
def managed_connection(host: str):
    """yield 之前=__enter__, yield 值=as 变量, yield 之后=__exit__"""
    conn = {"host": host, "connected": True}
    print(f"  [连接] {host}")
    try:
        yield conn
    finally:
        conn["connected"] = False
        print(f"  [断开] {host}")


def contextmanager_decorator_demo():
    """contextlib.contextmanager 装饰器演示"""
    print("\n" + "=" * 60)
    print("3. contextlib.contextmanager（yield 方式）")
    print("=" * 60)

    with managed_connection("localhost:5432") as conn:
        print(f"  使用连接: connected={conn['connected']}")
    print(f"  离开后: connected={conn['connected']}")

    # 另一个例子：用 yield 方式写计时器
    @contextlib.contextmanager
    def log_block(name):
        print(f"  >> 进入 {name}")
        yield
        print(f"  << 离开 {name}")

    with log_block("业务逻辑"):
        print(f"     执行中...")

    # Java 没有等价写法——必须写完整的类实现 AutoCloseable


# =============================================================================
# 4. contextlib.suppress —— 忽略特定异常
# =============================================================================

def suppress_demo():
    """contextlib.suppress 忽略特定异常"""
    print("\n" + "=" * 60)
    print("4. contextlib.suppress（忽略特定异常）")
    print("=" * 60)

    # 传统写法：
    # try:
    #     os.remove("file.txt")
    # except FileNotFoundError:
    #     pass

    # suppress 更优雅
    with contextlib.suppress(FileNotFoundError):
        os.remove("/tmp/_nonexistent_suppress.txt")
    print("  suppress(FileNotFoundError): 静默忽略")

    # 可同时忽略多种异常
    with contextlib.suppress(FileNotFoundError, PermissionError):
        os.remove("/tmp/_nonexistent_protected.txt")
    print("  suppress 多种异常: 同样静默")

    # Java 对比: 空 catch 块（被认为是反模式）
    # 注意：不要 suppress(Exception)——那是在掩盖 bug


# =============================================================================
# 5. contextlib.redirect_stdout
# =============================================================================

def redirect_stdout_demo():
    """捕获 stdout 输出到字符串"""
    print("\n" + "=" * 60)
    print("5. contextlib.redirect_stdout")
    print("=" * 60)

    # 将 print 输出捕获到 StringIO
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print("这行被捕获了")
        print("这行也是")
    print(f"  捕获内容: {buf.getvalue().strip()!r}")

    # redirect_stderr 捕获错误输出
    import sys
    err_buf = io.StringIO()
    with contextlib.redirect_stderr(err_buf):
        sys.stderr.write("错误输出\n")
    print(f"  捕获 stderr: {err_buf.getvalue().strip()!r}")

    # Java: System.setOut(new PrintStream(baos)) + 手动恢复
    # Python 的 with 自动恢复，更安全


# =============================================================================
# 6. ExitStack —— 动态管理多个上下文
# =============================================================================

def exit_stack_demo():
    """ExitStack：动态管理数量不定的上下文管理器"""
    print("\n" + "=" * 60)
    print("6. ExitStack（动态管理多个上下文）")
    print("=" * 60)

    # 场景：需要打开数量不定的资源
    tmp_dir = tempfile.gettempdir()
    paths = [os.path.join(tmp_dir, f"_stack_{i}.txt") for i in range(3)]
    for p in paths:
        with open(p, "w") as f:
            f.write(f"内容-{os.path.basename(p)}")

    # ExitStack 动态管理
    with contextlib.ExitStack() as stack:
        files = [stack.enter_context(open(p)) for p in paths]
        for f in files:
            print(f"  {os.path.basename(f.name)}: {f.read()}")
    print(f"  全部关闭? {all(f.closed for f in files)}")  # LIFO 关闭

    # 注册清理回调
    print("\n--- 清理回调（LIFO 顺序）---")
    with contextlib.ExitStack() as stack:
        stack.callback(print, "  回调C: 最先注册，最后执行")
        stack.callback(print, "  回调B: 第二")
        stack.callback(print, "  回调A: 最后注册，最先执行")
        print("  with 块执行中...")

    for p in paths:
        os.remove(p)


# =============================================================================
# 7. 自定义上下文管理器实例（数据库连接、计时器、临时目录）
# =============================================================================

@contextlib.contextmanager
def timer(label: str = "代码块"):
    """计时上下文管理器"""
    start = time.perf_counter()
    yield
    print(f"  [{label}] 耗时: {time.perf_counter() - start:.4f}s")


@contextlib.contextmanager
def temp_directory(prefix: str = "app_"):
    """创建临时目录，退出时自动删除"""
    path = tempfile.mkdtemp(prefix=prefix)
    try:
        yield path
    finally:
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        os.rmdir(path)
        print(f"  [清理] 临时目录已删除")


class DatabaseContext:
    """数据库事务上下文: 正常提交，异常回滚
    Java: try (Connection c = ds.getConnection()) { c.commit(); }"""

    def __init__(self, db: str):
        self.db = db

    def __enter__(self):
        print(f"  [DB] 连接 {self.db}，开始事务")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"  [DB] 回滚（{exc_val}）")
        else:
            print(f"  [DB] 提交事务")
        print(f"  [DB] 关闭连接")
        return False

    def execute(self, sql):
        print(f"  [DB] 执行: {sql}")


def custom_context_managers_demo():
    """自定义上下文管理器实例演示"""
    print("\n" + "=" * 60)
    print("7. 自定义上下文管理器实例")
    print("=" * 60)

    # 计时器
    print("--- 计时器 ---")
    with timer("求和"):
        total = sum(range(1_000_000))
    print(f"  结果: {total}")

    # 临时目录
    print("\n--- 临时目录 ---")
    with temp_directory("demo_") as tmp:
        tmp_file = os.path.join(tmp, "data.txt")
        with open(tmp_file, "w") as f:
            f.write("临时数据")
        print(f"  目录存在: {os.path.exists(tmp)}")
    print(f"  退出后: {os.path.exists(tmp)}")

    # 数据库（正常提交）
    print("\n--- 数据库（正常）---")
    with DatabaseContext("mydb") as db:
        db.execute("INSERT INTO users VALUES ('张三')")

    # 数据库（异常回滚）
    print("\n--- 数据库（异常回滚）---")
    try:
        with DatabaseContext("mydb") as db:
            db.execute("INSERT INTO orders VALUES (1)")
            raise ValueError("金额不合法")
    except ValueError:
        print("  外部处理完毕")


# =============================================================================
# 8. async with 异步上下文管理器简介
# =============================================================================

def async_context_manager_intro():
    """async with 异步上下文管理器简介"""

    print("\n" + "=" * 60)
    print("8. async with 异步上下文管理器简介")
    print("=" * 60)

    # 异步上下文管理器使用 __aenter__ / __aexit__
    print("  类方式: 实现 __aenter__ / __aexit__")
    print("    class AsyncDB:")
    print("        async def __aenter__(self):  return await connect()")
    print("        async def __aexit__(...):     await conn.close()")

    print("\n  装饰器方式: @contextlib.asynccontextmanager")
    print("    @asynccontextmanager")
    print("    async def async_db(host):")
    print("        conn = await connect(host)")
    print("        try:    yield conn")
    print("        finally: await conn.close()")

    print("\n  使用: async with async_db('host') as conn: ...")

    # Java 对比
    print("\n  Java 对比:")
    print("    Java try-with-resources 不支持异步")
    print("    需要 CompletableFuture 手动管理")

    print("\n  常见场景: aiohttp / aiofiles / asyncpg / motor")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    with_basics_demo()
    enter_exit_demo()
    contextmanager_decorator_demo()
    suppress_demo()
    redirect_stdout_demo()
    exit_stack_demo()
    custom_context_managers_demo()
    async_context_manager_intro()
