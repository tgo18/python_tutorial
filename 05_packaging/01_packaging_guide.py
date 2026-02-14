"""
Python3 打包构建指南 —— 写给 Java 开发者

核心概念：
- Python 的包管理生态经历了 pip -> Poetry -> uv 的演进
- 类比 Java: pip ≈ Maven, Poetry ≈ Gradle, uv ≈ "超级快的 Gradle"
- pyproject.toml 是现代 Python 项目的标准配置文件（类似 pom.xml）
"""


# =============================================================================
# 1. venv 虚拟环境
# =============================================================================

def venv_demo():
    """虚拟环境 —— 对比 Java 没有直接对应（类似 ClassLoader 隔离）"""

    print("=" * 60)
    print("1. venv 虚拟环境")
    print("=" * 60)

    # Java 的依赖隔离靠 Maven/Gradle 的项目级 classpath
    # Python 默认所有包装到全局 site-packages，需要 venv 做项目隔离

    print("""
    # --- 为什么需要虚拟环境？---
    # 场景：项目A 需要 requests==2.28，项目B 需要 requests==2.31
    # 没有 venv → 全局只能装一个版本，冲突！
    # Java 不需要：每个项目的 classpath 天然隔离

    # --- 创建虚拟环境 ---
    $ python -m venv .venv          # 在项目根目录创建 .venv 文件夹
    #                                 类似在项目里建了一个独立的 Python 环境

    # --- 激活虚拟环境 ---
    $ source .venv/bin/activate     # Linux/macOS
    $ .venv\\Scripts\\activate        # Windows
    # 激活后命令行前面会出现 (.venv) 提示符

    # --- 验证 ---
    $ which python                  # 应该指向 .venv/bin/python
    $ python --version              # 确认 Python 版本

    # --- 退出虚拟环境 ---
    $ deactivate                    # 回到系统全局 Python

    # --- 目录结构 ---
    # .venv/
    #   bin/              # 可执行文件 (python, pip, activate)
    #   lib/              # 安装的包 (site-packages)
    #   pyvenv.cfg        # 配置文件

    # --- 最佳实践 ---
    # 1. 将 .venv 加入 .gitignore（类似 Java 的 target/ 或 build/）
    # 2. 每个项目一个独立的 venv
    # 3. 使用 requirements.txt 记录依赖（后面会讲）
    """)


# =============================================================================
# 2. pip 包管理
# =============================================================================

def pip_demo():
    """pip 包管理 —— 对比 Java Maven/Gradle 依赖管理"""

    print("\n" + "=" * 60)
    print("2. pip 包管理")
    print("=" * 60)

    # pip 是 Python 的官方包管理器
    # 类比: pip install ≈ mvn dependency:resolve / gradle dependencies

    print("""
    # --- 安装包 ---
    $ pip install requests              # 安装最新版（≈ Maven 不指定版本）
    $ pip install requests==2.31.0      # 安装指定版本（≈ <version>2.31.0</version>）
    $ pip install "requests>=2.28,<3"   # 版本范围（≈ Maven version range）
    $ pip install requests[security]    # 安装可选依赖（≈ Maven optional dependency）

    # --- 卸载包 ---
    $ pip uninstall requests            # 移除包

    # --- 查看已安装 ---
    $ pip list                          # 列出所有包（≈ mvn dependency:tree 简化版）
    $ pip show requests                 # 查看包详情（版本、依赖、位置）

    # --- requirements.txt（类似 pom.xml 的 <dependencies>）---
    $ pip freeze > requirements.txt     # 导出当前环境的所有包和精确版本
    $ pip install -r requirements.txt   # 从文件安装（≈ mvn install）
    """)

    # 展示 requirements.txt 格式
    print("    # --- requirements.txt 文件格式 ---")
    requirements_example = """    requests==2.31.0
    flask==3.0.0
    sqlalchemy>=2.0,<3.0
    pytest>=7.0           # 开发依赖也混在一起（这是 pip 的缺点）
    # Java 的 Maven 有 <scope>test</scope>，pip 没有原生支持"""
    print(requirements_example)

    print("""
    # --- pip 的局限性（Java 开发者会觉得不方便的地方）---
    # 1. 没有 lock 文件 → 不同环境可能装到不同版本（Maven 有确定性构建）
    # 2. 没有 dev/test 依赖分组 → 生产和开发依赖混在一起
    # 3. 不能自动解决依赖冲突 → 可能出现版本不兼容
    # 4. 没有项目初始化命令 → 不像 mvn archetype:generate
    # → 这些问题催生了 Poetry 和 uv！
    """)


# =============================================================================
# 3. pyproject.toml 项目配置
# =============================================================================

def pyproject_demo():
    """pyproject.toml —— 对比 Java pom.xml / build.gradle"""

    print("\n" + "=" * 60)
    print("3. pyproject.toml 项目配置")
    print("=" * 60)

    # pyproject.toml 是 PEP 621 定义的标准项目配置文件
    # 类比: pyproject.toml ≈ pom.xml + build.gradle 的合体

    print("""
    # --- pyproject.toml 完整示例 ---

    [project]                               # ≈ Maven <project> 基本信息
    name = "my-awesome-app"                 # ≈ <artifactId>
    version = "1.0.0"                       # ≈ <version>
    description = "A demo project"          # ≈ <description>
    readme = "README.md"
    requires-python = ">=3.10"              # ≈ <maven.compiler.source>
    license = {text = "MIT"}                # ≈ <license>
    authors = [
        {name = "张三", email = "z@example.com"},  # ≈ <developers>
    ]
    dependencies = [                        # ≈ <dependencies>（运行时依赖）
        "requests>=2.28",
        "sqlalchemy>=2.0",
    ]

    [project.optional-dependencies]         # ≈ Maven profiles / Gradle configurations
    dev = [                                 # 开发依赖（≈ <scope>test</scope>）
        "pytest>=7.0",
        "black>=23.0",
        "mypy>=1.0",
    ]

    [project.scripts]                       # ≈ Maven exec plugin / Gradle application plugin
    my-cli = "my_app.cli:main"             # 注册命令行工具入口点

    [build-system]                          # ≈ Maven 的 <build><plugins> 或 Gradle plugins{}
    requires = ["setuptools>=68.0"]         # 构建工具（还有 hatchling, flit 等）
    build-backend = "setuptools.build_meta" # 构建后端

    [tool.pytest.ini_options]               # ≈ Maven surefire plugin 配置
    testpaths = ["tests"]
    addopts = "-v --tb=short"

    [tool.black]                            # 代码格式化配置（≈ checkstyle）
    line-length = 88

    [tool.mypy]                             # 类型检查配置（≈ Java 编译器类型检查）
    strict = true
    """)

    print("    # --- 对比总结 ---")
    print("    # pom.xml / build.gradle  →  pyproject.toml")
    print("    # <groupId>:<artifactId>  →  [project] name")
    print("    # <dependencies>          →  [project] dependencies")
    print("    # <build><plugins>        →  [build-system]")
    print("    # plugin 配置              →  [tool.*] 各工具配置")


# =============================================================================
# 4. Poetry 现代包管理
# =============================================================================

def poetry_demo():
    """Poetry —— 对比 Gradle 的完整项目管理"""

    print("\n" + "=" * 60)
    print("4. Poetry 现代包管理")
    print("=" * 60)

    # Poetry 解决了 pip 的大部分痛点
    # 类比: Poetry ≈ Gradle（依赖管理 + 构建 + 发布一体化）

    print("""
    # --- 安装 Poetry ---
    $ curl -sSL https://install.python-poetry.org | python3 -
    # 或: pipx install poetry

    # --- 初始化项目（≈ gradle init）---
    $ poetry init                       # 交互式创建 pyproject.toml
    $ poetry new my-project             # 创建完整项目结构（含 tests/）

    # --- 依赖管理 ---
    $ poetry add requests               # 添加依赖（≈ gradle 在 build.gradle 加依赖）
    $ poetry add pytest --group dev     # 添加开发依赖（≈ testImplementation）
    $ poetry remove requests            # 移除依赖

    # --- 安装与锁定 ---
    $ poetry install                    # 安装所有依赖（≈ gradle build）
    $ poetry lock                       # 生成/更新 poetry.lock
    #                                     lock 文件确保团队环境一致（≈ gradle.lockfile）

    # --- 构建与发布 ---
    $ poetry build                      # 打包成 wheel/sdist（≈ gradle jar）
    $ poetry publish                    # 发布到 PyPI（≈ gradle publish 到 Maven Central）

    # --- 运行 ---
    $ poetry run python main.py         # 在虚拟环境中运行
    $ poetry run pytest                 # 运行测试
    $ poetry shell                      # 进入虚拟环境 shell

    # --- Poetry 的优点 ---
    # 1. 自动管理虚拟环境
    # 2. poetry.lock 保证确定性构建
    # 3. 依赖分组 (main/dev/test)
    # 4. 一体化工具（init → develop → build → publish）

    # --- Poetry 的缺点（促使 uv 诞生）---
    # 1. 依赖解析速度慢（大项目可能要等几分钟）
    # 2. 安装本身就比较复杂
    # 3. 与 pip 生态不完全兼容
    # → 于是 uv 来了！
    """)


# =============================================================================
# 5. uv 新一代包管理（重点推荐！）
# =============================================================================

def uv_overview_demo():
    """uv 概览 —— Astral 出品，Rust 实现的超快包管理器"""

    print("\n" + "=" * 60)
    print("5. uv —— 新一代 Python 包管理（重点！）")
    print("=" * 60)

    print("""
    # ===== uv 是什么？=====
    # uv 是由 Astral（也是 ruff 代码检查工具的作者）用 Rust 开发的
    # Python 包管理工具。它是 pip + venv + Poetry + pipx 的全能替代品。
    #
    # 类比 Java: 想象一个用 C++ 重写的 Gradle，速度快 10-100 倍，
    #            而且完全兼容 Maven 仓库和 Gradle 的配置格式。
    #
    # 核心优势：
    # 1. 极快速度：Rust 实现，比 pip 快 10-100x（不是夸张）
    # 2. 全能：一个工具替代 pip + venv + poetry + pipx
    # 3. 兼容性：完全兼容 pip 和 pyproject.toml
    # 4. 确定性：自动生成 uv.lock 锁文件
    # 5. 零配置：开箱即用，不需要复杂安装

    # ===== 安装 uv =====
    $ curl -LsSf https://astral.sh/uv/install.sh | sh    # Linux/macOS
    # 或
    $ pip install uv          # 用 pip 安装（但推荐独立安装）
    # 或
    $ brew install uv         # macOS Homebrew
    """)


def uv_venv_and_pip_demo():
    """uv 替代 venv 和 pip"""

    print("\n" + "-" * 60)
    print("5.1 uv 替代 venv + pip")
    print("-" * 60)

    print("""
    # --- uv 创建虚拟环境（替代 python -m venv）---
    $ uv venv                      # 创建 .venv（比 python -m venv 快 10 倍）
    $ uv venv --python 3.12        # 指定 Python 版本（自动下载！）
    $ uv venv myenv                # 自定义目录名

    # 注意：uv 可以自动检测和下载 Python 版本！
    # Java 开发者类比：像 sdkman 一样管理多个 Python 版本

    # --- uv pip（替代 pip，完全兼容的 pip 命令）---
    $ uv pip install requests              # 安装包（比 pip 快 10-100x）
    $ uv pip install -r requirements.txt   # 从 requirements.txt 安装
    $ uv pip uninstall requests            # 卸载
    $ uv pip list                          # 列出已安装包
    $ uv pip freeze                        # 导出依赖
    $ uv pip compile requirements.in -o requirements.txt  # 依赖锁定

    # --- 速度对比（真实场景）---
    # pip install django         → ~15 秒
    # uv pip install django      → ~0.5 秒     （快 30 倍！）
    # pip install -r big-req.txt → ~120 秒
    # uv pip install -r big.txt  → ~2 秒       （快 60 倍！）
    """)


def uv_project_demo():
    """uv 项目管理（替代 Poetry）"""

    print("\n" + "-" * 60)
    print("5.2 uv 项目管理（替代 Poetry）")
    print("-" * 60)

    print("""
    # --- 初始化项目（≈ poetry new / gradle init）---
    $ uv init my-project               # 创建新项目
    $ cd my-project
    # 自动生成：
    #   pyproject.toml    ← 项目配置
    #   .python-version   ← Python 版本
    #   hello.py          ← 示例代码
    #   README.md

    # --- 添加依赖（≈ poetry add / gradle dependencies）---
    $ uv add requests                  # 添加运行时依赖
    $ uv add "flask>=3.0"             # 带版本约束
    $ uv add pytest --dev              # 添加开发依赖（≈ testImplementation）
    $ uv remove requests               # 移除依赖

    # uv add 会自动：
    # 1. 更新 pyproject.toml（加入 dependencies）
    # 2. 解析依赖树（解决冲突）
    # 3. 更新 uv.lock 锁文件
    # 4. 安装到虚拟环境
    # 一条命令完成 Java 中需要"修改 pom.xml + mvn install"两步的工作

    # --- 同步依赖（≈ poetry install / mvn install）---
    $ uv sync                          # 安装 pyproject.toml 中的所有依赖
    $ uv sync --frozen                 # 严格按照 uv.lock 安装（CI 推荐）
    $ uv sync --no-dev                 # 只安装生产依赖（部署时用）

    # --- 运行代码 ---
    $ uv run python main.py            # 在项目环境中运行（自动同步依赖）
    $ uv run pytest                    # 运行测试
    $ uv run flask run                 # 运行 Flask 服务

    # uv run 的魔力：自动创建 venv + 安装依赖 + 运行命令，一步到位！
    # Java 类比：像 gradle run 一样，不需要先手动构建
    """)


def uv_lock_demo():
    """uv.lock 锁文件机制"""

    print("\n" + "-" * 60)
    print("5.3 uv.lock 锁文件")
    print("-" * 60)

    print("""
    # --- uv.lock 是什么？---
    # uv.lock 类似 package-lock.json (npm) 或 gradle.lockfile
    # 它记录了所有依赖的精确版本和哈希值，确保：
    # 1. 团队所有人安装完全相同的版本
    # 2. CI/CD 构建结果可复现
    # 3. 防止"在我机器上能跑"的问题

    # --- 工作流程 ---
    $ uv add requests          # 自动更新 uv.lock
    $ uv lock                  # 手动重新生成锁文件
    $ uv sync --frozen         # 严格按锁文件安装（不更新 lock）

    # --- 最佳实践 ---
    # 1. uv.lock 必须提交到 Git（和 poetry.lock 一样）
    # 2. CI 中使用 uv sync --frozen 确保一致性
    # 3. 升级依赖时用 uv lock --upgrade

    # --- 对比 ---
    # pip freeze > requirements.txt  → 手动、容易忘记更新
    # poetry.lock                    → 自动但解析慢
    # uv.lock                        → 自动且极快（推荐！）
    """)


def uv_tool_demo():
    """uv tool（替代 pipx）"""

    print("\n" + "-" * 60)
    print("5.4 uv tool install（替代 pipx）")
    print("-" * 60)

    print("""
    # --- 什么是 uv tool？---
    # 用于安装全局 CLI 工具，每个工具有独立的隔离环境
    # 类比：像 npx (npm) 或者全局安装的 CLI 工具

    $ uv tool install ruff             # 安装代码检查工具
    $ uv tool install black            # 安装代码格式化工具
    $ uv tool install httpie           # 安装 HTTP 客户端
    $ uv tool list                     # 列出已安装的工具
    $ uv tool uninstall ruff           # 卸载工具

    # --- uvx: 临时运行工具（≈ npx）---
    $ uvx ruff check .                 # 不安装，直接临时运行 ruff
    $ uvx black --check .             # 临时运行 black 检查格式
    $ uvx cowsay "Hello Python!"       # 甚至可以跑小工具
    # uvx 会自动下载、缓存、运行，用完即走
    """)


def uv_why_recommend_demo():
    """为什么推荐 uv"""

    print("\n" + "-" * 60)
    print("5.5 为什么推荐 uv（总结）")
    print("-" * 60)

    print("""
    # ===== 工具对比一览 =====
    #
    # 功能            pip          Poetry       uv
    # ──────────────────────────────────────────────────────
    # 安装包          pip install  poetry add   uv add / uv pip install
    # 虚拟环境        python -m venv  自动管理  uv venv（可自动下载 Python）
    # 锁文件          无（手动 freeze） poetry.lock uv.lock
    # 依赖分组        无           有           有
    # 构建/发布       twine        poetry build uv build / uv publish
    # 全局工具        pipx         无           uv tool
    # 速度            慢           中等         极快（10-100x）
    # 实现语言        Python       Python       Rust
    #
    # ===== 推荐策略 =====
    # 新项目 → 直接用 uv（2024年后的最佳选择）
    # 老项目用 pip → 可以无缝切换到 uv pip（完全兼容）
    # 老项目用 Poetry → 可以逐步迁移到 uv（兼容 pyproject.toml）
    #
    # ===== 完整的 uv 工作流 =====
    $ uv init my-project && cd my-project   # 1. 创建项目
    $ uv add flask sqlalchemy               # 2. 添加依赖
    $ uv add pytest --dev                   # 3. 添加开发依赖
    $ uv run pytest                         # 4. 运行测试
    $ uv run python -m my_app               # 5. 运行应用
    $ uv build                              # 6. 打包
    $ uv publish                            # 7. 发布到 PyPI
    """)

    # 用 Java 做最终类比
    print("    # --- Java 开发者的终极类比 ---")
    print("    # uv init         ≈  gradle init")
    print("    # uv add          ≈  添加到 build.gradle + gradle build")
    print("    # uv sync         ≈  gradle dependencies + build")
    print("    # uv run          ≈  gradle run")
    print("    # uv lock         ≈  gradle --write-locks")
    print("    # uv build        ≈  gradle jar")
    print("    # uv publish      ≈  gradle publish")
    print("    # uv tool install ≈  全局安装 CLI（Java 没有直接对应）")


# =============================================================================
# 6. pytest 测试
# =============================================================================

def pytest_demo():
    """pytest 测试框架 —— 对比 Java JUnit"""

    print("\n" + "=" * 60)
    print("6. pytest 测试框架")
    print("=" * 60)

    # --- 基本测试 ---
    print("\n--- 6.1 基本测试（≈ JUnit @Test）---")

    def add(a, b):
        return a + b

    def test_add():
        """最简单的测试函数"""
        # Python: 直接用 assert
        # Java:   assertEquals(3, add(1, 2))
        assert add(1, 2) == 3
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    test_add()
    print("    test_add 通过!")

    print("""
    # --- 测试文件结构 ---
    # my_project/
    #   src/
    #     calculator.py
    #   tests/
    #     test_calculator.py    # 文件名必须 test_ 开头
    #     conftest.py           # 共享 fixture（≈ JUnit @BeforeAll 的集中管理）
    #
    # 运行: $ pytest                    # 自动发现并运行所有 test_*.py
    #       $ pytest tests/test_calc.py  # 运行特定文件
    #       $ pytest -v                  # 详细输出
    #       $ pytest -k "test_add"       # 按名称过滤
    """)

    # --- Fixture ---
    print("--- 6.2 Fixture（≈ JUnit @BeforeEach / @BeforeAll）---")

    print("""
    import pytest

    @pytest.fixture                    # ≈ JUnit @BeforeEach
    def sample_user():
        '''每个测试前创建新用户'''
        user = {"name": "张三", "age": 30}
        yield user                     # yield 之前 = setUp, 之后 = tearDown
        # 这里可以做清理工作（≈ @AfterEach）
        print("清理用户数据")

    @pytest.fixture(scope="module")    # ≈ JUnit @BeforeAll
    def db_connection():
        '''整个模块共享一个数据库连接'''
        conn = create_connection()
        yield conn
        conn.close()                   # 模块结束后关闭

    def test_user_name(sample_user):   # 参数名 = fixture 函数名，自动注入！
        assert sample_user["name"] == "张三"

    # Java 需要 @Autowired 或 @BeforeEach 手动创建
    # Python 的 fixture 通过参数名自动注入，更简洁！
    """)

    # --- 参数化测试 ---
    print("--- 6.3 参数化测试（≈ JUnit @ParameterizedTest）---")

    import pytest  # noqa: F811

    # 模拟参数化测试
    test_data = [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ]

    print("""
    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ])
    def test_add_parametrized(a, b, expected):
        assert add(a, b) == expected

    # Java JUnit 5 等价代码：
    # @ParameterizedTest
    # @CsvSource({"1,2,3", "0,0,0", "-1,1,0", "100,200,300"})
    # void testAdd(int a, int b, int expected) {
    #     assertEquals(expected, Calculator.add(a, b));
    # }
    """)

    # 实际运行参数化测试
    for a, b, expected in test_data:
        assert add(a, b) == expected
        print(f"    test_add({a}, {b}) == {expected} 通过!")

    # --- Mock ---
    print("\n--- 6.4 Mock（≈ Java Mockito）---")

    print("""
    from unittest.mock import Mock, patch, MagicMock

    # --- 基本 Mock ---
    mock_service = Mock()                          # ≈ Mockito.mock(Service.class)
    mock_service.get_user.return_value = "张三"     # ≈ when(...).thenReturn(...)
    assert mock_service.get_user(1) == "张三"
    mock_service.get_user.assert_called_once_with(1)  # ≈ verify(mock).getUser(1)

    # --- patch 替换模块中的对象（≈ @MockBean / @InjectMocks）---
    @patch("my_app.service.requests.get")
    def test_fetch_data(mock_get):
        mock_get.return_value.json.return_value = {"key": "value"}
        result = fetch_data("http://api.example.com")
        assert result == {"key": "value"}
        mock_get.assert_called_once()

    # --- MagicMock 自动生成属性和方法 ---
    mock_db = MagicMock()
    mock_db.query.filter_by.return_value.first.return_value = "结果"
    # 链式调用随便写，MagicMock 全都接受（类似 Mockito 的 deep stubs）
    """)

    # 实际演示 Mock
    from unittest.mock import Mock

    mock_api = Mock()
    mock_api.get_data.return_value = {"status": "ok", "count": 42}
    result = mock_api.get_data("users")
    print(f"    Mock 返回: {result}")
    mock_api.get_data.assert_called_once_with("users")
    print("    Mock 验证通过!")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    venv_demo()
    pip_demo()
    pyproject_demo()
    poetry_demo()
    uv_overview_demo()
    uv_venv_and_pip_demo()
    uv_project_demo()
    uv_lock_demo()
    uv_tool_demo()
    uv_why_recommend_demo()
    pytest_demo()
