"""
Python3 pathlib & os —— 写给 Java 开发者

核心概念：
- pathlib 是 Python 3.4+ 的面向对象文件路径库（推荐）
- 类比 Java: pathlib.Path ≈ java.nio.file.Path
- os.path 是旧式 API，类似 Java 的 java.io.File
"""

from pathlib import Path
import os
import tempfile


# =============================================================================
# 1. Path 对象创建
# =============================================================================

def path_creation():
    """Path 对象创建 vs Java Paths.get()"""

    print("=" * 60)
    print("Path 对象创建")
    print("=" * 60)

    # Java: Path p = Paths.get("/home", "user", "docs");
    p = Path("/home", "user", "docs")
    print(f"多参数构造: {p}")

    # Java: Path p = Paths.get("/home/user/docs");
    print(f"字符串构造: {Path('/home/user/docs')}")

    # Java: Paths.get("").toAbsolutePath()
    print(f"当前目录: {Path.cwd()}")

    # Java: System.getProperty("user.home")
    print(f"用户主目录: {Path.home()}")

    # 相对路径 -> 绝对路径
    relative = Path("src", "main")
    print(f"相对路径: {relative}")
    print(f"转绝对路径: {relative.resolve()}")


# =============================================================================
# 2. 路径操作
# =============================================================================

def path_operations():
    """路径操作 —— / 运算符是 Python 的独特优势"""

    print("\n" + "=" * 60)
    print("路径操作")
    print("=" * 60)

    # / 运算符拼接 —— Java: path.resolve("user").resolve("docs")
    full = Path("/home") / "user" / "docs" / "report.txt"
    print(f"/ 拼接: {full}")

    # 路径组件 —— Java: path.getParent(), path.getFileName()
    print(f"parent: {full.parent}, name: {full.name}")
    print(f"stem: {full.stem}, suffix: {full.suffix}")
    print(f"parts: {full.parts}")

    # 多层后缀 —— .tar.gz 场景
    archive = Path("/data/backup.tar.gz")
    print(f"\nsuffix: {archive.suffix}, suffixes: {archive.suffixes}")

    # 修改文件名/后缀 —— Java 没有直接方法
    print(f"\nwith_name:   {full.with_name('summary.txt')}")
    print(f"with_suffix: {full.with_suffix('.md')}")
    print(f"with_stem:   {full.with_stem('notes')}")

    # 遍历所有父目录
    print(f"\n所有父目录: {[str(p) for p in full.parents]}")


# =============================================================================
# 3. 文件读写
# =============================================================================

def file_read_write():
    """文件读写 —— 简洁的一行式 API"""

    print("\n" + "=" * 60)
    print("文件读写")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # 写文件 —— Java: Files.writeString(path, content);
        hello = tmp / "hello.txt"
        hello.write_text("你好，世界！\nHello, World!", encoding="utf-8")

        # 读文件 —— Java: String content = Files.readString(path);
        print(f"读取内容: {hello.read_text(encoding='utf-8')}")

        # 二进制读写 —— Java: Files.write(path, bytes);
        binary_file = tmp / "data.bin"
        binary_file.write_bytes(b"\x00\x01\x02\x03")
        print(f"二进制数据: {binary_file.read_bytes().hex()}")

        # 追加模式 —— Java: StandardOpenOption.APPEND
        log = tmp / "app.log"
        log.write_text("第一行\n", encoding="utf-8")
        with log.open("a", encoding="utf-8") as f:
            f.write("第二行\n")
            f.write("第三行\n")
        print(f"追加后共 {len(log.read_text(encoding='utf-8').splitlines())} 行")

        # 创建多层目录 —— Java: Files.createDirectories(path);
        nested = tmp / "a" / "b" / "c"
        nested.mkdir(parents=True, exist_ok=True)
        (nested / "deep.txt").write_text("深层文件", encoding="utf-8")
        print(f"深层文件已创建: {(nested / 'deep.txt').exists()}")


# =============================================================================
# 4. 目录遍历
# =============================================================================

def directory_traversal():
    """目录遍历 —— iterdir, glob, rglob"""

    print("\n" + "=" * 60)
    print("目录遍历")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # 构建演示目录结构
        for d in ["src", "tests", "docs"]:
            (tmp / d).mkdir()
        for name, text in [("src/main.py", "# main"), ("src/utils.py", "# utils"),
                           ("tests/test_main.py", "# test"), ("docs/readme.md", "# doc"),
                           ("setup.py", "# setup")]:
            (tmp / name).write_text(text, encoding="utf-8")

        # iterdir(): 列出直接子项 —— Java: Files.list(dir)
        print("iterdir（直接子项）:")
        for item in sorted(tmp.iterdir()):
            kind = "目录" if item.is_dir() else "文件"
            print(f"  [{kind}] {item.name}")

        # glob(): 模式匹配 —— Java: DirectoryStream
        print("\nglob('*.py'):")
        for f in sorted(tmp.glob("*.py")):
            print(f"  {f.name}")

        # rglob(): 递归匹配 —— Java: Files.walk(dir)
        print("\nrglob('*.py')（递归）:")
        for f in sorted(tmp.rglob("*.py")):
            print(f"  {f.relative_to(tmp)}")


# =============================================================================
# 5. 文件信息
# =============================================================================

def file_info():
    """文件信息 —— stat, exists, is_file, is_dir"""

    print("\n" + "=" * 60)
    print("文件信息")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        demo = tmp / "demo.txt"
        demo.write_text("Hello " * 100, encoding="utf-8")

        # 存在性检查 —— Java: Files.exists(path)
        print(f"exists: {demo.exists()}, is_file: {demo.is_file()}, is_dir: {demo.is_dir()}")

        # stat —— Java: Files.size(), Files.getLastModifiedTime()
        st = demo.stat()
        from datetime import datetime
        print(f"\n大小: {st.st_size} 字节, "
              f"修改: {datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")

        # 不存在的路径
        ghost = tmp / "not_here.txt"
        print(f"\n不存在: exists={ghost.exists()}, is_file={ghost.is_file()}")

        # 删除文件 —— Java: Files.delete / Files.deleteIfExists
        demo.unlink()
        print(f"删除后 exists: {demo.exists()}")
        demo.unlink(missing_ok=True)  # 不抛异常
        print("missing_ok=True 不报错")


# =============================================================================
# 6. os 模块常用功能
# =============================================================================

def os_module_demo():
    """os 模块 —— 操作系统交互"""

    print("\n" + "=" * 60)
    print("os 模块常用功能")
    print("=" * 60)

    # 环境变量 —— Java: System.getenv("HOME")
    print(f"HOME: {os.environ.get('HOME', '未设置')}")
    print(f"PATH 前60字符: {os.environ.get('PATH', '')[:60]}...")
    print(f"DEBUG（默认值）: {os.environ.get('DEBUG', 'false')}")

    # 当前目录 —— Java: System.getProperty("user.dir")
    print(f"\n当前目录: {os.getcwd()}")

    # makedirs —— Java: new File(path).mkdirs()
    with tempfile.TemporaryDirectory() as tmpdir:
        deep = os.path.join(tmpdir, "a", "b", "c")
        os.makedirs(deep, exist_ok=True)
        print(f"创建多级目录: {os.path.exists(deep)}")

    # 操作系统信息
    print(f"\n操作系统: {os.name}")            # posix / nt
    print(f"路径分隔符: {os.sep}")
    print(f"行结束符: {repr(os.linesep)}")
    print(f"CPU 核心数: {os.cpu_count()}")


# =============================================================================
# 7. os.path vs pathlib 对比
# =============================================================================

def ospath_vs_pathlib():
    """os.path vs pathlib —— 推荐使用 pathlib"""

    print("\n" + "=" * 60)
    print("os.path vs pathlib 对比（推荐 pathlib）")
    print("=" * 60)

    fp = "/home/user/projects/app/main.py"

    # 拼接路径
    print("拼接路径:")
    print(f"  os.path.join:  {os.path.join('/home', 'user', 'docs')}")
    print(f"  pathlib /    : {Path('/home') / 'user' / 'docs'}")

    # 获取文件名
    print(f"\n文件名:  os.path={os.path.basename(fp)}, pathlib={Path(fp).name}")

    # 获取父目录
    print(f"父目录:  os.path={os.path.dirname(fp)}, pathlib={Path(fp).parent}")

    # 分离后缀
    name, ext = os.path.splitext(fp)
    print(f"\n后缀: os.path=({os.path.basename(name)}, {ext}), "
          f"pathlib=(stem={Path(fp).stem}, suffix={Path(fp).suffix})")

    # 判断存在
    print(f"\n存在: os.path={os.path.exists('/tmp')}, pathlib={Path('/tmp').exists()}")

    # 绝对路径
    print(f"绝对: os.path={os.path.abspath('.')}, pathlib={Path('.').resolve()}")

    print("\n结论: pathlib 面向对象，代码更简洁，新代码推荐使用")


# =============================================================================
# 8. tempfile 临时文件
# =============================================================================

def tempfile_demo():
    """tempfile —— 安全地创建临时文件和目录"""

    print("\n" + "=" * 60)
    print("tempfile 临时文件")
    print("=" * 60)

    # NamedTemporaryFile —— Java: Files.createTempFile()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", prefix="demo_") as f:
        f.write("临时内容")
        f.flush()
        print(f"临时文件: {f.name}")
        print(f"文件存在: {Path(f.name).exists()}")
    print(f"退出后已删除: {not Path(f.name).exists()}")

    # TemporaryDirectory —— Java: Files.createTempDirectory()
    with tempfile.TemporaryDirectory(prefix="myapp_") as tmpdir:
        tmp = Path(tmpdir)
        print(f"\n临时目录: {tmp}")
        (tmp / "data.csv").write_text("a,b,c\n1,2,3", encoding="utf-8")
        (tmp / "sub").mkdir()
        (tmp / "sub" / "config.yaml").write_text("key: val", encoding="utf-8")
        print(f"文件数: {len(list(tmp.rglob('*')))}")
    print(f"退出后已清理: {not Path(tmpdir).exists()}")

    # mkstemp: 低级 API，不自动删除
    fd, path = tempfile.mkstemp(suffix=".log", prefix="app_")
    try:
        os.write(fd, b"low level temp\n")
        os.close(fd)
        print(f"\nmkstemp: {path}")
        print(f"内容: {Path(path).read_text().strip()}")
    finally:
        os.unlink(path)
        print(f"手动清理: {not Path(path).exists()}")

    # 系统临时目录 —— Java: System.getProperty("java.io.tmpdir")
    print(f"\n系统临时目录: {tempfile.gettempdir()}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    path_creation()
    path_operations()
    file_read_write()
    directory_traversal()
    file_info()
    os_module_demo()
    ospath_vs_pathlib()
    tempfile_demo()
