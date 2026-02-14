"""
Python3 异常处理 —— 写给 Java 开发者

核心概念：
- Python 没有 checked exception，所有异常都是 unchecked
- 类比 Java: try-except-else-finally vs try-catch-finally
- Python 推崇 EAFP（先做再说），Java 推崇 LBYL（先查再做）
"""

import warnings


# ============================================================
# 1. try-except 基础 —— 对比 Java try-catch
# ============================================================

def basic_try_except_demo():
    """try-except 基础用法"""
    print("=" * 60)
    print("1. try-except 基础（对比 Java try-catch）")
    print("=" * 60)

    # Java: try { ... } catch (ArithmeticException e) { ... }
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"  捕获除零错误: {e}")

    try:
        print(f"  访问越界: {[1, 2, 3][10]}")
    except IndexError as e:
        print(f"  捕获索引越界: {e}  类型: {type(e).__name__}")

    # 捕获通用 Exception（不推荐，太宽泛）
    try:
        int("not_a_number")
    except Exception as e:
        print(f"  通用捕获: {type(e).__name__}: {e}")


# ============================================================
# 2. 多异常捕获 —— 对比 Java multi-catch
# ============================================================

def multi_exception_demo():
    """多种异常的捕获方式"""
    print("\n" + "=" * 60)
    print("2. 多异常捕获（对比 Java multi-catch）")
    print("=" * 60)

    # Java 7+: catch (IOException | SQLException e)
    def safe_divide(a, b):
        try:
            return a / b
        except (ZeroDivisionError, TypeError) as e:
            print(f"  元组捕获 -> {type(e).__name__}: {e}")
            return None

    safe_divide(10, 0)
    safe_divide("10", 3)

    # 分别处理（对应 Java 的多个 catch 块）
    def parse_and_access(text, index):
        try:
            return [int(text) * i for i in range(1, 4)][index]
        except ValueError as e:
            print(f"  解析失败: {e}")
        except IndexError as e:
            print(f"  索引越界: {e}")

    parse_and_access("abc", 0)
    parse_and_access("10", 99)
    print(f"  正常调用: {parse_and_access('5', 1)}")


# ============================================================
# 3. else 和 finally —— 对比 Java try-catch-finally
# ============================================================

def else_finally_demo():
    """Python 独有的 else 子句 + finally"""
    print("\n" + "=" * 60)
    print("3. else 和 finally（Python 比 Java 多了 else）")
    print("=" * 60)

    # Java 只有 try-catch-finally；Python 多了 else（无异常时执行）
    def divide(a, b):
        try:
            result = a / b
        except ZeroDivisionError:
            print("  [except]  除零错误!")
        else:
            print(f"  [else]    结果 = {result}")  # 无异常才执行
        finally:
            print(f"  [finally] 清理资源，a={a}, b={b}")

    print("--- 正常 ---")
    divide(10, 3)
    print("--- 异常 ---")
    divide(10, 0)


# ============================================================
# 4. 异常层次结构 —— 对比 Java Exception hierarchy
# ============================================================

def exception_hierarchy_demo():
    """Python 异常的继承体系"""
    print("\n" + "=" * 60)
    print("4. 异常层次结构（对比 Java Exception hierarchy）")
    print("=" * 60)

    # Java: Throwable -> Error / Exception -> RuntimeException
    print("""  BaseException                 # ~ Throwable
  +-- SystemExit                # ~ System.exit()，别捕获
  +-- KeyboardInterrupt         # Ctrl+C，别捕获
  +-- Exception                 # ~ Exception（日常用这个）
      +-- ValueError            # ~ IllegalArgumentException
      +-- TypeError             # ~ ClassCastException
      +-- KeyError              # ~ NoSuchElementException
      +-- IndexError            # ~ IndexOutOfBoundsException
      +-- FileNotFoundError     # ~ FileNotFoundException
      +-- OSError               # ~ IOException""")

    print("\n  关键: Python 没有 checked exception，全是 unchecked")
    print("  except Exception 不捕获 KeyboardInterrupt/SystemExit")


# ============================================================
# 5. 自定义异常 —— 对比 Java custom exceptions
# ============================================================

# Python: 继承 Exception（Java 需 extends RuntimeException）
class BusinessError(Exception):
    """业务异常基类"""
    def __init__(self, code: str, message: str):
        self.code, self.message = code, message
        super().__init__(f"[{code}] {message}")

class OrderNotFoundError(BusinessError):
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__("ORDER_404", f"订单 {order_id} 不存在")

class InsufficientBalanceError(BusinessError):
    def __init__(self, required: float, available: float):
        self.required, self.available = required, available
        super().__init__("BALANCE_ERR", f"需要 {required:.2f}，余额仅 {available:.2f}")

def custom_exception_demo():
    """自定义异常演示"""
    print("\n" + "=" * 60)
    print("5. 自定义异常（对比 Java custom exceptions）")
    print("=" * 60)

    def process_order(oid, amount, balance):
        if oid <= 0:    raise OrderNotFoundError(oid)
        if amount > balance: raise InsufficientBalanceError(amount, balance)
        return f"订单 {oid} 支付成功，扣款 {amount:.2f}"

    for oid, amt, bal in [(1001, 50, 100), (-1, 50, 100), (1002, 200, 100)]:
        try:
            print(f"  成功: {process_order(oid, amt, bal)}")
        except OrderNotFoundError as e:
            print(f"  订单错误: {e} (id={e.order_id})")
        except InsufficientBalanceError as e:
            print(f"  余额错误: {e} (差额={e.required - e.available:.2f})")
        except BusinessError as e:
            print(f"  业务异常: {e.code} - {e.message}")


# ============================================================
# 6. 异常链 (raise ... from ...) —— 对比 Java initCause
# ============================================================

def exception_chaining_demo():
    """异常链：保留原始异常的上下文"""
    print("\n" + "=" * 60)
    print("6. 异常链 raise...from...（对比 Java initCause）")
    print("=" * 60)

    # Java: throw new ServiceException("msg", cause);
    def get_user(uid):
        try:
            raise ConnectionError(f"无法连接数据库 (id={uid})")
        except ConnectionError as e:
            raise BusinessError("DB_ERR", "用户查询失败") from e

    try:
        get_user(42)
    except BusinessError as e:
        print(f"  业务异常: {e}")
        print(f"  原始原因: {e.__cause__}")
        print(f"  原因类型: {type(e.__cause__).__name__}")

    # 隐式链 __context__ vs 显式链 __cause__（from）
    try:
        try:
            1 / 0
        except ZeroDivisionError:
            raise ValueError("转换失败")  # 隐式设置 __context__
    except ValueError as e:
        print(f"  隐式 __context__: {e.__context__}")

    # from None 切断异常链
    try:
        try:
            int("abc")
        except ValueError:
            raise BusinessError("PARSE_ERR", "无效输入") from None
    except BusinessError as e:
        print(f"  from None 切断链: __cause__={e.__cause__}")


# ============================================================
# 7. 上下文管理器与异常 (with 语句简介)
# ============================================================

def context_manager_demo():
    """with 语句自动处理资源清理"""
    print("\n" + "=" * 60)
    print("7. 上下文管理器与异常（with 语句简介）")
    print("=" * 60)

    # Java 7+: try (Resource r = ...) { ... }  （AutoCloseable）
    class DBConn:
        def __init__(self, name): self.name = name
        def __enter__(self):
            print(f"  [enter] 连接: {self.name}")
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                print(f"  [exit]  异常: {exc_type.__name__}: {exc_val}")
            print(f"  [exit]  关闭: {self.name}")
            return False  # False=不吞异常, True=吞掉
        def query(self, sql):
            if "DROP" in sql: raise PermissionError("禁止 DROP!")
            return f"结果: [{sql}]"

    print("--- 正常 ---")
    with DBConn("mydb") as c:
        print(f"  {c.query('SELECT * FROM users')}")

    print("\n--- 异常（资源仍被清理）---")
    try:
        with DBConn("mydb") as c:
            c.query("DROP TABLE users")
    except PermissionError as e:
        print(f"  外部捕获: {e}")


# ============================================================
# 8. EAFP vs LBYL —— Python "先做再说" vs Java "先检查再做"
# ============================================================

def eafp_vs_lbyl_demo():
    """两种编程风格对比"""
    print("\n" + "=" * 60)
    print("8. EAFP vs LBYL 编程风格")
    print("=" * 60)

    user = {"name": "张三", "age": 28}

    # LBYL (Look Before You Leap) —— Java: if (map.containsKey(...))
    print("--- LBYL（Java 习惯）---")
    phone = user["phone"] if "phone" in user else "未设置"
    print(f"  电话: {phone}")

    # EAFP (Easier to Ask Forgiveness than Permission)
    print("--- EAFP（Python 推崇）---")
    try:
        phone = user["phone"]
    except KeyError:
        phone = "未设置"
    print(f"  电话: {phone}")
    print(f"  最地道: {user.get('phone', '未设置')}")  # dict.get()

    # EAFP 避免 TOCTOU 竞态
    print("\n--- 文件操作 EAFP（避免竞态）---")
    try:
        with open("/tmp/_nonexistent_demo.txt") as f:
            f.read()
    except FileNotFoundError:
        print("  文件不存在，安全处理")

    # 鸭子类型 + EAFP
    print("\n--- 鸭子类型与 EAFP ---")
    class Duck:
        def quack(self): return "嘎嘎!"
    for obj in [Duck(), "not_a_duck"]:
        try:
            print(f"  {type(obj).__name__}: {obj.quack()}")
        except AttributeError:
            print(f"  {type(obj).__name__}: 不会叫")


# ============================================================
# 9. warnings 模块简介
# ============================================================

def warnings_demo():
    """warnings：没严重到抛异常，但需要提醒开发者"""
    print("\n" + "=" * 60)
    print("9. warnings 模块简介")
    print("=" * 60)

    # 类似 Java @Deprecated，但 Python 在运行时发出
    def old_api(x):
        warnings.warn("old_api() 已弃用，请用 new_api()",
                       DeprecationWarning, stacklevel=2)
        return x * 2

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        print(f"  old_api(5) = {old_api(5)}")
        if caught:
            w = caught[0]
            print(f"  警告类别: {w.category.__name__}")
            print(f"  警告内容: {w.message}")

    print("\n  常见警告类型:")
    for name, desc in [
        ("DeprecationWarning",  "功能已弃用 (~ @Deprecated)"),
        ("FutureWarning",       "未来版本行为将改变"),
        ("UserWarning",         "通用用户警告"),
        ("RuntimeWarning",      "运行时可疑行为"),
    ]:
        print(f"    {name:<24s} {desc}")


# ============================================================
# 运行所有 demo
# ============================================================

if __name__ == "__main__":
    basic_try_except_demo()
    multi_exception_demo()
    else_finally_demo()
    exception_hierarchy_demo()
    custom_exception_demo()
    exception_chaining_demo()
    context_manager_demo()
    eafp_vs_lbyl_demo()
    warnings_demo()
