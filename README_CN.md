# Python3 系统学习指南 —— 写给 Java 架构师

## 学习路线总览

本教程专为有 Java 经验的后端工程师设计，通过对比 Java 的方式快速掌握 Python3 核心知识。

## 目录结构

```
python_tutorial/
├── 01_syntax/          # 第一章：语法基础
├── 02_concurrency/     # 第二章：并发编程
├── 03_stdlib/          # 第三章：常用标准库
├── 04_frameworks/      # 第四章：主流框架
├── 05_packaging/       # 第五章：打包构建
└── requirements.txt    # 项目依赖
```

## 学习计划

### 第一阶段：语法基础 (`01_syntax/`)

| 序号 | 主题 | 文件 | Java 对比 |
|------|------|------|-----------|
| 1 | 类型与变量 | `01_types_and_variables.py` | 动态类型 vs 静态类型 |
| 2 | 控制流 | `02_control_flow.py` | match-case vs switch |
| 3 | 函数 | `03_functions.py` | 一等公民 vs 方法 |
| 4 | 面向对象 | `04_oop.py` | 多继承、MRO vs 单继承+接口 |
| 5 | 装饰器 | `05_decorators.py` | AOP / 注解 的 Python 方式 |
| 6 | 生成器与迭代器 | `06_generators_iterators.py` | Stream API 的 Python 方式 |
| 7 | 类型提示 | `07_type_hints.py` | Python 也能"静态类型" |
| 8 | 异常处理 | `08_error_handling.py` | try-except vs try-catch |
| 9 | 推导式 | `09_comprehensions.py` | Python 独有的优雅语法 |

### 第二阶段：并发编程 (`02_concurrency/`)

| 序号 | 主题 | 文件 | Java 对比 |
|------|------|------|-----------|
| 1 | 多线程 | `01_threading_basics.py` | GIL 限制 vs Java 真并行 |
| 2 | 多进程 | `02_multiprocessing.py` | 突破 GIL 的方式 |
| 3 | asyncio | `03_asyncio_basics.py` | 协程 vs CompletableFuture |
| 4 | concurrent.futures | `04_concurrent_futures.py` | 类似 ExecutorService |
| 5 | 同步原语 | `05_sync_primitives.py` | Lock/Event/Semaphore |

### 第三阶段：常用标准库 (`03_stdlib/`)

| 序号 | 主题 | 文件 | Java 对比 |
|------|------|------|-----------|
| 1 | collections | `01_collections_module.py` | 增强容器 |
| 2 | itertools | `02_itertools_module.py` | Stream 工具集 |
| 3 | pathlib & os | `03_pathlib_and_os.py` | java.nio.file.Path |
| 4 | logging | `04_logging_module.py` | SLF4J / Logback |
| 5 | JSON 与序列化 | `05_json_and_serialization.py` | Jackson / Gson |
| 6 | 正则表达式 | `06_re_module.py` | java.util.regex |
| 7 | dataclasses | `07_dataclasses_module.py` | Lombok @Data / Record |
| 8 | 上下文管理器 | `08_contextmanager.py` | try-with-resources |
| 9 | 数字与数学 | `09_numbers_and_math.py` | BigDecimal / Math |
| 10 | 日期与时间 | `10_datetime_module.py` | java.time (LocalDateTime/ZonedDateTime) |

### 第四阶段：主流框架 (`04_frameworks/`)

| 序号 | 主题 | 目录 | Java 对比 |
|------|------|------|-----------|
| 1 | Flask | `flask_demo/` | 轻量 Web，类比 Spring Boot 极简版 |
| 2 | FastAPI | `fastapi_demo/` | 现代异步 Web，自带 OpenAPI |
| 3 | SQLAlchemy | `sqlalchemy_demo/` | ORM，类比 MyBatis / JPA |

### 第五阶段：打包构建 (`05_packaging/`)

| 序号 | 主题 | 说明 | Java 对比 |
|------|------|------|-----------|
| 1 | venv | 虚拟环境隔离 | 无直接对应（类似 classloader 隔离） |
| 2 | pip | 包管理 | Maven / Gradle 依赖管理 |
| 3 | pyproject.toml | 项目配置 | pom.xml / build.gradle |
| 4 | Poetry | 现代包管理工具 | 类似 Gradle |
| 5 | uv | 新一代包管理（Rust 实现） | 速度类比 Gradle vs Maven 的提升 |
| 6 | 测试 | pytest | JUnit |

## 快速开始

```bash
# 1. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行任意 demo
python3 01_syntax/01_types_and_variables.py
```

## 核心差异速查（Java vs Python）

| 维度 | Java | Python |
|------|------|--------|
| 类型系统 | 静态强类型 | 动态强类型 |
| 编译/解释 | 编译为字节码（JVM） | 解释执行（CPython） |
| 并发模型 | 真多线程 | GIL 限制，多进程/协程补偿 |
| 包管理 | Maven/Gradle | pip/Poetry/uv |
| 项目构建 | pom.xml/build.gradle | pyproject.toml |
| Web 框架 | Spring Boot | Flask/FastAPI/Django |
| ORM | JPA/MyBatis | SQLAlchemy/Django ORM |
| 接口/抽象 | interface/abstract | ABC(Abstract Base Class)/Protocol |
| Lambda | `(x) -> x + 1` | `lambda x: x + 1` |
| 空值 | `null` | `None` |
| 入口 | `public static void main` | `if __name__ == "__main__"` |
