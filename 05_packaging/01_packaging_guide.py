"""
Python3 打包构建指南 —— 写给 Java 开发者

核心概念：
- Python 的包管理生态经历了 pip -> Poetry -> uv 的演进
- 类比 Java: pip ≈ Maven, Poetry ≈ Gradle, uv ≈ "超级快的 Gradle"
- pyproject.toml 是现代 Python 项目的标准配置文件（类似 pom.xml）
"""

from unittest.mock import Mock


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
    # 项目A 需要 requests==2.28，项目B 需要 requests==2.31
    # 没有 venv → 全局只能装一个版本，冲突！
    # Java 不需要：每个项目的 classpath 天然隔离

    # --- 创建 & 使用 ---
    $ python -m venv .venv          # 创建 .venv 文件夹
    $ source .venv/bin/activate     # Linux/macOS 激活
    $ .venv\\Scripts\\activate        # Windows 激活
    $ which python                  # 应指向 .venv/bin/python
    $ deactivate                    # 退出虚拟环境

    # --- 最佳实践 ---
    # 1. 将 .venv 加入 .gitignore（类似 Java 的 target/）
    # 2. 每个项目一个独立的 venv
    """)


# =============================================================================
# 2. pip 包管理
# =============================================================================

def pip_demo():
    """pip 包管理 —— 对比 Java Maven/Gradle 依赖管理"""

    print("\n" + "=" * 60)
    print("2. pip 包管理")
    print("=" * 60)

    print("""
    # --- 安装 / 卸载 ---
    $ pip install requests              # 安装最新版
    $ pip install requests==2.31.0      # 指定版本（≈ <version>2.31.0</version>）
    $ pip install "requests>=2.28,<3"   # 版本范围（≈ Maven version range）
    $ pip uninstall requests            # 卸载

    # --- 查看 & 导出 ---
    $ pip list                          # 列出所有包
    $ pip show requests                 # 查看包详情
    $ pip freeze > requirements.txt     # 导出精确版本（≈ pom.xml dependencies）
    $ pip install -r requirements.txt   # 从文件安装（≈ mvn install）

    # --- pip 的局限性 ---
    # 1. 没有 lock 文件 → 不同环境可能装到不同版本
    # 2. 没有 dev/test 依赖分组 → 生产和开发依赖混在一起
    # 3. 不能自动解决依赖冲突
    # → 这些痛点催生了 Poetry 和 uv！
    """)


# =============================================================================
# 3. pyproject.toml 项目配置
# =============================================================================

def pyproject_demo():
    """pyproject.toml —— 对比 Java pom.xml / build.gradle"""

    print("\n" + "=" * 60)
    print("3. pyproject.toml 项目配置")
    print("=" * 60)

    # PEP 621 标准配置文件，≈ pom.xml + build.gradle 的合体
    print("""
    [project]                               # ≈ Maven <project> 基本信息
    name = "my-awesome-app"                 # ≈ <artifactId>
    version = "1.0.0"                       # ≈ <version>
    description = "A demo project"
    requires-python = ">=3.10"              # ≈ <maven.compiler.source>
    dependencies = ["requests>=2.28", "sqlalchemy>=2.0"]  # ≈ <dependencies>

    [project.optional-dependencies]         # ≈ Maven profiles
    dev = ["pytest>=7.0", "black>=23.0", "mypy>=1.0"]

    [project.scripts]                       # ≈ Gradle application plugin
    my-cli = "my_app.cli:main"             # 命令行入口点

    [build-system]                          # ≈ Maven <build><plugins>
    requires = ["setuptools>=68.0"]
    build-backend = "setuptools.build_meta"

    [tool.pytest.ini_options]               # ≈ surefire plugin
    testpaths = ["tests"]

    [tool.black]                            # 代码格式化（≈ checkstyle）
    line-length = 88
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

    # Poetry ≈ Gradle（依赖管理 + 构建 + 发布一体化）
    print("""
    $ curl -sSL https://install.python-poetry.org | python3 -  # 安装

    $ poetry init                       # 交互式创建 pyproject.toml（≈ gradle init）
    $ poetry new my-project             # 创建完整项目结构（含 tests/）
    $ poetry add requests               # 添加依赖（≈ build.gradle 加依赖）
    $ poetry add pytest --group dev     # 开发依赖（≈ testImplementation）
    $ poetry install                    # 安装所有依赖（≈ gradle build）
    $ poetry lock                       # 生成 poetry.lock（确保团队一致）
    $ poetry build                      # 打包（≈ gradle jar）
    $ poetry publish                    # 发布到 PyPI
    $ poetry run python main.py         # 在虚拟环境中运行
    $ poetry run pytest                 # 运行测试

    # --- Poetry 的缺点（促使 uv 诞生）---
    # 1. 依赖解析速度慢（大项目可能等几分钟）
    # 2. 安装本身比较复杂
    # 3. 与 pip 生态不完全兼容 → 于是 uv 来了！
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
    # Astral（ruff 的作者）用 Rust 开发的 Python 包管理工具
    # 它是 pip + venv + Poetry + pipx 的全能替代品
    #
    # 类比: 想象一个用 C++ 重写的 Gradle，快 10-100 倍，完全兼容现有生态
    #
    # 核心优势：
    # 1. 极快：Rust 实现，比 pip 快 10-100x
    # 2. 全能：一个工具替代 pip + venv + poetry + pipx
    # 3. 兼容：完全兼容 pip 和 pyproject.toml
    # 4. 确定性：自动生成 uv.lock 锁文件
    # 5. 零配置：开箱即用

    # ===== 安装 =====
    $ curl -LsSf https://astral.sh/uv/install.sh | sh    # Linux/macOS
    $ pip install uv                                       # 或用 pip
    $ brew install uv                                      # 或 Homebrew
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
    # 类比：像 sdkman 一样自动管理多个 Python 版本

    # --- uv pip（完全兼容的 pip 替代品）---
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
    # 自动生成：pyproject.toml, .python-version, hello.py, README.md

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
    # 一条命令完成 Java 中"修改 pom.xml + mvn install"两步的工作

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
    # 类似 package-lock.json (npm) 或 gradle.lockfile
    # 记录所有依赖的精确版本和哈希值，确保团队环境一致、CI 可复现

    $ uv add requests          # 自动更新 uv.lock
    $ uv lock                  # 手动重新生成锁文件
    $ uv lock --upgrade        # 升级所有依赖到最新兼容版本
    $ uv sync --frozen         # 严格按锁文件安装（CI 推荐！）

    # 最佳实践：uv.lock 必须提交到 Git，CI 用 --frozen 确保一致性
    # 对比：pip freeze 手动易忘 / poetry.lock 自动但慢 / uv.lock 自动且极快
    """)


def uv_tool_demo():
    """uv tool（替代 pipx）"""

    print("\n" + "-" * 60)
    print("5.4 uv tool install（替代 pipx）")
    print("-" * 60)

    print("""
    # 安装全局 CLI 工具，每个工具有独立隔离环境（类比 npx）
    $ uv tool install ruff             # 安装代码检查工具
    $ uv tool install black            # 安装代码格式化工具
    $ uv tool list                     # 列出已安装的工具
    $ uv tool uninstall ruff           # 卸载

    # --- uvx: 临时运行（≈ npx）---
    $ uvx ruff check .                 # 不安装，直接临时运行
    $ uvx black --check .             # 临时检查格式
    $ uvx cowsay "Hello Python!"       # 自动下载、缓存、运行，用完即走
    """)


def uv_why_recommend_demo():
    """为什么推荐 uv"""

    print("\n" + "-" * 60)
    print("5.5 为什么推荐 uv（总结）")
    print("-" * 60)

    print("""
    # ===== 工具对比 =====
    #  功能        pip            Poetry         uv
    # ──────────────────────────────────────────────────
    #  安装包      pip install    poetry add     uv add
    #  虚拟环境    python -m venv 自动管理       uv venv（可自动下载 Python）
    #  锁文件      无(手动freeze) poetry.lock    uv.lock
    #  构建/发布   twine          poetry build   uv build / uv publish
    #  全局工具    pipx           无             uv tool
    #  速度        慢             中等           极快（10-100x）
    #  实现语言    Python         Python         Rust

    # 推荐：新项目直接用 uv，老项目可无缝迁移（兼容 pip / pyproject.toml）

    # ===== 完整 uv 工作流 =====
    $ uv init my-project && cd my-project   # 1. 创建项目
    $ uv add flask sqlalchemy               # 2. 添加依赖
    $ uv add pytest --dev                   # 3. 开发依赖
    $ uv run pytest                         # 4. 测试
    $ uv build                              # 5. 打包
    $ uv publish                            # 6. 发布
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

    # Python: 直接用 assert；Java: assertEquals(3, add(1, 2))
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    print("    test_add 通过!")

    print("""
    # 测试文件: tests/test_*.py（文件名必须 test_ 开头）
    # 共享配置: tests/conftest.py（共享 fixture）
    # 运行: $ pytest             # 自动发现所有 test_*.py
    #       $ pytest -v          # 详细输出
    #       $ pytest -k "add"    # 按名称过滤
    """)

    # --- Fixture ---
    print("--- 6.2 Fixture（≈ JUnit @BeforeEach / @BeforeAll）---")
    print("""
    import pytest

    @pytest.fixture                    # ≈ JUnit @BeforeEach
    def sample_user():
        user = {"name": "张三", "age": 30}
        yield user                     # yield 前 = setUp, 后 = tearDown
        print("清理用户数据")          # ≈ @AfterEach

    @pytest.fixture(scope="module")    # ≈ JUnit @BeforeAll（模块级共享）
    def db_connection():
        conn = create_connection()
        yield conn
        conn.close()

    def test_user_name(sample_user):   # 参数名 = fixture 名 → 自动注入！
        assert sample_user["name"] == "张三"
    """)

    # --- 参数化测试 ---
    print("--- 6.3 参数化测试（≈ JUnit @ParameterizedTest）---")
    print("""
    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),  (0, 0, 0),  (-1, 1, 0),  (100, 200, 300),
    ])
    def test_add_parametrized(a, b, expected):
        assert add(a, b) == expected

    # Java: @ParameterizedTest + @CsvSource({"1,2,3", "0,0,0"})
    """)

    # 实际运行参数化测试演示
    test_data = [(1, 2, 3), (0, 0, 0), (-1, 1, 0), (100, 200, 300)]
    for a, b, expected in test_data:
        assert add(a, b) == expected
        print(f"    test_add({a}, {b}) == {expected} 通过!")

    # --- Mock ---
    print("\n--- 6.4 Mock（≈ Java Mockito）---")
    print("""
    from unittest.mock import Mock, patch, MagicMock

    mock_svc = Mock()                             # ≈ Mockito.mock(Service.class)
    mock_svc.get_user.return_value = "张三"        # ≈ when(...).thenReturn(...)
    mock_svc.get_user.assert_called_once_with(1)  # ≈ verify(mock).getUser(1)

    @patch("my_app.service.requests.get")          # ≈ @MockBean
    def test_fetch_data(mock_get):
        mock_get.return_value.json.return_value = {"key": "value"}

    mock_db = MagicMock()                          # ≈ Mockito deep stubs
    mock_db.query.filter_by.return_value.first.return_value = "结果"
    """)

    # 实际演示 Mock
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
