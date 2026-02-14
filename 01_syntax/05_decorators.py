"""
Python3 装饰器 —— 写给 Java 开发者

核心概念：
- 装饰器本质是"高阶函数"：接收函数作为参数，返回新函数
- 类比 Java: @Transactional, @Cacheable 等注解 + AOP 切面
- 但 Python 装饰器更灵活：不需要框架支持，纯语言特性
"""

import functools
import time
from typing import Callable, Any


# =============================================================================
# 1. 基础装饰器
# =============================================================================

def basic_decorator_demo():
    """理解装饰器的本质"""

    print("=" * 60)
    print("基础装饰器")
    print("=" * 60)

    # 装饰器的本质就是函数包装
    def my_decorator(func):
        @functools.wraps(func)  # 保留原函数的元信息（名称、文档等）
        def wrapper(*args, **kwargs):
            print(f"  [Before] 调用 {func.__name__}")
            result = func(*args, **kwargs)
            print(f"  [After] {func.__name__} 返回 {result}")
            return result
        return wrapper

    # 使用 @ 语法糖
    @my_decorator
    def add(a, b):
        """加法函数"""
        return a + b

    # @my_decorator 等价于: add = my_decorator(add)
    result = add(3, 5)
    print(f"  结果: {result}")
    print(f"  函数名: {add.__name__}")  # 'add'（因为 @wraps）
    print(f"  文档: {add.__doc__}")


# =============================================================================
# 2. 实用装饰器示例
# =============================================================================

# --- 计时装饰器（类似 Java AOP 的性能监控）---
def timer(func):
    """记录函数执行时间"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  ⏱ {func.__name__} 耗时: {elapsed:.4f}s")
        return result
    return wrapper


# --- 重试装饰器（类似 Spring Retry）---
def retry(max_attempts: int = 3, delay: float = 1.0):
    """带参数的装饰器：自动重试"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"  [Retry] {func.__name__} 第{attempt}次失败: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay * 0.01)  # demo 用短延迟
            raise last_exception
        return wrapper
    return decorator


# --- 缓存装饰器（类似 @Cacheable）---
def memoize(func):
    """简单缓存（Python 内置 @functools.lru_cache 更好用）"""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
            print(f"  [Cache MISS] {func.__name__}{args}")
        else:
            print(f"  [Cache HIT] {func.__name__}{args}")
        return cache[args]
    return wrapper


# --- 日志装饰器 ---
def log_call(func):
    """记录函数调用参数和返回值"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"  -> {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"  <- {func.__name__} = {result!r}")
        return result
    return wrapper


def practical_decorators_demo():
    """实用装饰器演示"""

    print("\n" + "=" * 60)
    print("实用装饰器")
    print("=" * 60)

    # 计时
    @timer
    def slow_function():
        total = sum(range(1000000))
        return total

    print("--- 计时装饰器 ---")
    slow_function()

    # 重试
    call_count = 0

    @retry(max_attempts=3, delay=0.1)
    def unreliable_api():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("网络超时")
        return "成功"

    print("\n--- 重试装饰器 ---")
    result = unreliable_api()
    print(f"  最终结果: {result}")

    # 缓存
    @memoize
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print("\n--- 缓存装饰器 ---")
    print(f"  fib(10) = {fibonacci(10)}")

    # Python 内置的缓存装饰器（推荐使用）
    @functools.lru_cache(maxsize=128)
    def fib_cached(n):
        if n < 2:
            return n
        return fib_cached(n - 1) + fib_cached(n - 2)

    print(f"  fib_cached(50) = {fib_cached(50)}")
    print(f"  缓存统计: {fib_cached.cache_info()}")


# =============================================================================
# 3. 带参数的装饰器
# =============================================================================

def parameterized_decorator_demo():
    """带参数的装饰器（三层嵌套）"""

    print("\n" + "=" * 60)
    print("带参数的装饰器")
    print("=" * 60)

    # 权限检查（类似 Spring Security 的 @PreAuthorize）
    def require_role(*roles):
        """检查用户角色"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 模拟获取当前用户角色
                current_role = kwargs.get("_role", "guest")
                if current_role not in roles:
                    raise PermissionError(
                        f"需要角色 {roles}，当前角色: {current_role}"
                    )
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @require_role("admin", "superadmin")
    def delete_user(user_id, _role=None):
        return f"已删除用户 {user_id}"

    # 有权限
    print(f"  {delete_user(42, _role='admin')}")

    # 无权限
    try:
        delete_user(42, _role="guest")
    except PermissionError as e:
        print(f"  权限不足: {e}")


# =============================================================================
# 4. 类装饰器
# =============================================================================

def class_decorator_demo():
    """类装饰器 & 用类实现装饰器"""

    print("\n" + "=" * 60)
    print("类装饰器")
    print("=" * 60)

    # 1. 用类实现装饰器（利用 __call__）
    class CountCalls:
        """统计函数被调用的次数"""

        def __init__(self, func):
            functools.update_wrapper(self, func)
            self.func = func
            self.call_count = 0

        def __call__(self, *args, **kwargs):
            self.call_count += 1
            return self.func(*args, **kwargs)

    @CountCalls
    def say_hello(name):
        return f"Hello, {name}"

    say_hello("张三")
    say_hello("李四")
    say_hello("王五")
    print(f"  say_hello 被调用了 {say_hello.call_count} 次")

    # 2. 装饰器装饰类（类似 Java 的 @Component）
    registry = {}

    def register(cls):
        """注册类到全局注册表"""
        registry[cls.__name__] = cls
        return cls

    @register
    class UserService:
        def get_user(self, id):
            return f"User-{id}"

    @register
    class OrderService:
        def get_order(self, id):
            return f"Order-{id}"

    print(f"\n  已注册的服务: {list(registry.keys())}")
    service = registry["UserService"]()
    print(f"  {service.get_user(1)}")


# =============================================================================
# 5. 装饰器叠加
# =============================================================================

def stacking_demo():
    """装饰器叠加（执行顺序）"""

    print("\n" + "=" * 60)
    print("装饰器叠加")
    print("=" * 60)

    @log_call
    @timer
    def process_data(data):
        """处理数据"""
        return [x * 2 for x in data]

    # 叠加顺序：从下往上包装，从上往下执行
    # 等价于: process_data = log_call(timer(process_data))
    # 执行顺序: log_call 先执行 -> timer 再执行 -> 原函数

    result = process_data([1, 2, 3])
    print(f"  结果: {result}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    basic_decorator_demo()
    practical_decorators_demo()
    parameterized_decorator_demo()
    class_decorator_demo()
    stacking_demo()
