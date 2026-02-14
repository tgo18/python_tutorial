"""
Python3 logging 模块 —— 写给 Java 开发者

核心概念：
- Python 内置 logging 模块，架构和 Java 的 Logback/Log4j 极其相似
- 类比 Java: Logger + Handler + Formatter ≈ Logger + Appender + Layout
"""

import logging
import logging.handlers
import sys
import tempfile
import os


# =============================================================================
# 1. 基础用法
# =============================================================================

def basic_usage():
    """基础日志输出 —— 对比 Java SLF4J logger.info()"""

    print("=" * 60)
    print("1. 基础用法")
    print("=" * 60)

    # Java: LoggerFactory.getLogger(MyClass.class).info("Hello {}", name);
    # Python: 直接使用模块级函数（操作 root logger，默认级别 WARNING）
    logging.warning("这是一条 warning 日志")
    logging.error("这是一条 error 日志")

    # 字符串格式化
    name = "张三"
    logging.warning("用户 %s 登录失败", name)   # % 风格（惰性求值，推荐）
    logging.warning(f"用户 {name} 登录失败")     # f-string（立即求值）
    # Java 对比: logger.warn("用户 {} 登录失败", name);


# =============================================================================
# 2. 日志级别
# =============================================================================

def log_levels():
    """日志级别 —— 对比 Java log levels"""

    print("\n" + "=" * 60)
    print("2. 日志级别")
    print("=" * 60)

    # Python 级别(数值)   Java 对应:  DEBUG(10) INFO(20) WARNING(30) ERROR(40) CRITICAL(50)
    for name, val in [("DEBUG", 10), ("INFO", 20), ("WARNING(默认)", 30),
                      ("ERROR", 40), ("CRITICAL", 50)]:
        print(f"  {name:15s} = {val}")

    # 创建独立 logger 演示级别过滤
    logger = logging.getLogger("level_demo")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    print("\n  级别=DEBUG，全部输出：")
    logger.debug("  DEBUG 级别")
    logger.info("  INFO 级别")
    logger.warning("  WARNING 级别")

    handler.setLevel(logging.WARNING)
    print("\n  handler 级别=WARNING，只输出 WARNING+：")
    logger.info("  被过滤")
    logger.warning("  WARNING 通过")
    logger.removeHandler(handler)


# =============================================================================
# 3. Logger + Handler + Formatter 架构
# =============================================================================

def architecture_demo():
    """Logger, Handler, Formatter —— 对比 Java Logback 架构"""

    print("\n" + "=" * 60)
    print("3. Logger + Handler + Formatter 架构")
    print("=" * 60)

    # Python:  Logger ----> Handler  ----> Formatter
    # Java:    Logger ----> Appender ----> Layout

    logger = logging.getLogger("myapp.arch")           # 步骤1: Logger
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler(sys.stdout)        # 步骤2: Handler
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(                     # 步骤3: Formatter
        "%(asctime)s [%(levelname)-8s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    console.setFormatter(formatter)                    # 步骤4: 组装
    logger.addHandler(console)

    print("  组装完毕：")
    logger.info("服务启动成功")
    logger.warning("连接池快满了")

    # Java Logback XML 对比:
    # <appender name="STDOUT" class="ConsoleAppender">
    #   <encoder><pattern>%d [%-8level] %logger - %msg%n</pattern></encoder>
    # </appender>
    logger.removeHandler(console)


# =============================================================================
# 4. 文件 Handler
# =============================================================================

def file_handler_demo():
    """文件 Handler —— FileHandler + RotatingFileHandler"""

    print("\n" + "=" * 60)
    print("4. 文件 Handler")
    print("=" * 60)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    with tempfile.TemporaryDirectory() as tmpdir:
        # --- FileHandler（对比 Java FileAppender）---
        log_file = os.path.join(tmpdir, "app.log")
        logger = logging.getLogger("file_demo")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        logger.info("写入文件 - 1")
        logger.warning("写入文件 - 2")
        fh.close()
        logger.removeHandler(fh)

        with open(log_file, encoding="utf-8") as f:
            print("  FileHandler 输出:")
            for line in f:
                print(f"    {line.rstrip()}")

        # --- RotatingFileHandler（对比 Java RollingFileAppender）---
        rot_file = os.path.join(tmpdir, "rotating.log")
        rh = logging.handlers.RotatingFileHandler(
            rot_file, maxBytes=500, backupCount=3, encoding="utf-8")
        rh.setFormatter(fmt)
        rot_logger = logging.getLogger("rotating_demo")
        rot_logger.setLevel(logging.DEBUG)
        rot_logger.addHandler(rh)
        for i in range(20):
            rot_logger.info(f"Rotating message #{i:03d}")
        rh.close()
        rot_logger.removeHandler(rh)

        files = sorted(f for f in os.listdir(tmpdir) if f.startswith("rotating"))
        print("\n  RotatingFileHandler 文件轮转:")
        for fname in files:
            size = os.path.getsize(os.path.join(tmpdir, fname))
            print(f"    {fname} ({size} bytes)")
        # 另有 TimedRotatingFileHandler（按时间轮转）


# =============================================================================
# 5. 日志格式化
# =============================================================================

def format_demo():
    """日志格式化 —— 对比 Java PatternLayout"""

    print("\n" + "=" * 60)
    print("5. 日志格式化")
    print("=" * 60)

    # Python 字段              Java Logback Pattern
    # %(asctime)s              %d{yyyy-MM-dd HH:mm:ss}
    # %(name)s                 %logger
    # %(levelname)s            %level / %(message)s  %msg
    # %(filename)s:%(lineno)d  %file:%line
    # %(threadName)s           %thread
    formats = {
        "简洁": "%(levelname)s - %(message)s",
        "标准": "%(asctime)s [%(levelname)-8s] %(name)s - %(message)s",
        "详细": "%(asctime)s %(filename)s:%(lineno)d - %(message)s",
        "线程": "%(asctime)s [%(threadName)s] %(levelname)s - %(message)s",
    }

    logger = logging.getLogger("fmt_demo")
    logger.setLevel(logging.DEBUG)
    for style_name, fmt in formats.items():
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(fmt, datefmt="%H:%M:%S"))
        logger.addHandler(h)
        print(f"\n  [{style_name}] ", end="")
        logger.info("用户登录")
        logger.removeHandler(h)


# =============================================================================
# 6. 多模块日志 (getLogger(__name__))
# =============================================================================

def multi_module_demo():
    """多模块日志 —— 对比 Java LoggerFactory.getLogger(Class)"""

    print("\n" + "=" * 60)
    print("6. 多模块日志")
    print("=" * 60)

    # Java: LoggerFactory.getLogger(UserService.class);
    # Python: logging.getLogger(__name__)
    # 名称用 . 分隔形成层级（类似 Java 包名）

    parent = logging.getLogger("webapp")
    parent.setLevel(logging.DEBUG)
    ph = logging.StreamHandler(sys.stdout)
    ph.setFormatter(logging.Formatter(
        "[%(name)-20s] %(levelname)-8s %(message)s"))
    parent.addHandler(ph)

    svc = logging.getLogger("webapp.service")   # 子 logger 自动继承父 handler
    db = logging.getLogger("webapp.database")

    print("  子 logger 继承父 handler：")
    svc.info("处理请求")
    db.warning("连接池 > 80%")

    db.setLevel(logging.WARNING)
    print("\n  database 级别=WARNING：")
    db.info("被过滤")
    db.warning("通过过滤")

    # propagate 控制传播（默认 True）
    child = logging.getLogger("webapp.child")
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter("  CHILD> %(message)s"))
    child.addHandler(ch)

    print("\n  propagate=True，日志输出两次：")
    child.warning("重复演示")
    child.propagate = False
    print("  propagate=False，只输出一次：")
    child.warning("不再重复")

    parent.removeHandler(ph)
    child.removeHandler(ch)
    child.propagate = True


# =============================================================================
# 7. 结构化日志和最佳实践
# =============================================================================

def best_practices():
    """结构化日志和最佳实践"""

    print("\n" + "=" * 60)
    print("7. 结构化日志和最佳实践")
    print("=" * 60)

    logger = logging.getLogger("practices")
    logger.setLevel(logging.DEBUG)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter("  %(levelname)s - %(message)s"))
    logger.addHandler(h)

    # [1] 每个模块用 __name__
    print("  [1] logger = logging.getLogger(__name__)")
    print("      Java: LoggerFactory.getLogger(MyClass.class)")

    # [2] % 格式化（惰性求值）优于 f-string
    logger.info("用户 %d 操作成功", 42)
    print("  [2] 用 %s/%d 惰性格式化，性能更好")

    # [3] logger.exception() 自动记录异常堆栈
    print("\n  [3] logger.exception() 记录堆栈：")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("计算失败")  # Java: logger.error("失败", e);

    # [4] extra 传递结构化上下文
    print("\n  [4] extra 传递上下文：")
    ctx_h = logging.StreamHandler(sys.stdout)
    ctx_h.setFormatter(logging.Formatter(
        "  %(levelname)s [user=%(user_id)s] %(message)s"))
    ctx = logging.getLogger("practices.ctx")
    ctx.addHandler(ctx_h)
    ctx.propagate = False
    ctx.info("订单创建", extra={"user_id": "U123"})
    ctx.removeHandler(ctx_h)
    ctx.propagate = True

    # [5] 应用入口统一配置
    print("\n  [5] 入口配置（类似 logback.xml）:")
    print("    logging.basicConfig(level=logging.INFO,")
    print("        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s')")

    # [6] dictConfig 生产级配置
    print("\n  [6] dictConfig 集中管理:")
    print("    logging.config.dictConfig({'version': 1, ...})")

    logger.removeHandler(h)


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    basic_usage()
    log_levels()
    architecture_demo()
    file_handler_demo()
    format_demo()
    multi_module_demo()
    best_practices()
