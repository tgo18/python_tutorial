"""
Python3 正则表达式 re 模块 —— 写给 Java 开发者

核心概念：
- Python 的 re 模块和 Java 的 java.util.regex 功能基本一致
- 类比 Java: re.compile() ≈ Pattern.compile()
- Python 用 r"" 原始字符串避免反斜杠转义问题
"""

import re


# =============================================================================
# 1. re.match / re.search / re.fullmatch
# =============================================================================

def match_search_fullmatch_demo():
    """
    匹配函数三兄弟 —— 对比 Java Pattern/Matcher

    Java: m.find() ≈ re.search()       从任意位置找
    Java: m.matches() ≈ re.fullmatch() 整个字符串匹配
    Java: m.lookingAt() ≈ re.match()   从开头匹配
    """
    print("=" * 60)
    print("1. re.match / re.search / re.fullmatch")
    print("=" * 60)

    text = "abc123def456"

    # re.match：只匹配字符串开头（Java Matcher.lookingAt()）
    m1 = re.match(r"\d+", text)
    print(f"  match(r'\\d+', '{text}'): {m1}")              # None，开头不是数字
    m2 = re.match(r"[a-z]+", text)
    print(f"  match(r'[a-z]+', '{text}'): {m2.group()}")    # 'abc'

    # re.search：扫描整个字符串，找第一个匹配（Java Matcher.find()）
    m3 = re.search(r"\d+", text)
    print(f"  search(r'\\d+', '{text}'): {m3.group()}")     # '123'
    print(f"    位置: start={m3.start()}, end={m3.end()}")

    # re.fullmatch：整个字符串必须完全匹配（Java Matcher.matches()）
    m4 = re.fullmatch(r"\w+", text)
    print(f"  fullmatch(r'\\w+', '{text}'): {m4.group()}")  # 整个串
    m5 = re.fullmatch(r"\d+", text)
    print(f"  fullmatch(r'\\d+', '{text}'): {m5}")          # None

    # 匹配对象的常用方法
    m = re.search(r"(\d+)", text)
    print(f"\n  匹配对象: group()={m.group()}, span()={m.span()}, string={m.string}")


# =============================================================================
# 2. re.findall / re.finditer
# =============================================================================

def findall_finditer_demo():
    """
    查找所有匹配 —— 对比 Java while(matcher.find()) 循环收集
    """
    print("\n" + "=" * 60)
    print("2. re.findall / re.finditer")
    print("=" * 60)

    text = "价格: 苹果12.5元, 香蕉3.8元, 西瓜25元"

    # findall：返回所有匹配的字符串列表
    prices = re.findall(r"\d+\.?\d*", text)
    print(f"  findall 所有价格: {prices}")    # ['12.5', '3.8', '25']

    # 注意坑：findall 有分组时，只返回分组内容！
    pairs = re.findall(r"(\w+?)(\d+\.?\d*)元", text)
    print(f"  findall 有分组: {pairs}")       # 返回元组列表
    # finditer：返回匹配对象的迭代器（大数据量时更省内存）
    print("  finditer 迭代:")
    for m in re.finditer(r"\d+\.?\d*", text):
        print(f"    '{m.group()}' at [{m.start()}:{m.end()}]")


# =============================================================================
# 3. 分组捕获 (?P<name>...)
# =============================================================================

def named_group_demo():
    """
    命名分组 —— 对比 Java: Pattern.compile("(?<year>\\d{4})")
    Python 语法: (?P<name>...)  注意比 Java 多了个 P
    """
    print("\n" + "=" * 60)
    print("3. 分组捕获 (?P<name>...)")
    print("=" * 60)

    date_str = "2025-06-15 14:30:00"

    # 普通分组（按编号访问）
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    print(f"  普通分组: groups()={m.groups()}")
    # 命名分组（按名称访问，可读性更好）
    pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    m = re.search(pattern, date_str)
    print(f"  命名分组: year={m.group('year')}, month={m.group('month')}")
    print(f"  groupdict() = {m.groupdict()}")   # 返回字典！
    # 实战：命名分组 + finditer 解析日志
    log = "[ERROR] 2025-06-15 10:30 - 连接超时 | [WARN] 2025-06-15 10:31 - 重试中"
    log_pat = r"\[(?P<level>\w+)\]\s+(?P<date>[\d-]+)\s+(?P<time>[\d:]+)\s+-\s+(?P<msg>.+?)(?:\s*\||$)"
    print(f"\n  解析日志:")
    for m in re.finditer(log_pat, log):
        d = m.groupdict()
        print(f"    {d['level']:>5} | {d['date']} {d['time']} | {d['msg']}")


# =============================================================================
# 4. re.sub 替换
# =============================================================================

def sub_demo():
    """
    正则替换 —— 对比 Java Matcher.replaceAll() / replaceFirst()
    Python: re.sub(pattern, repl, string, count=0)
    """
    print("\n" + "=" * 60)
    print("4. re.sub 替换")
    print("=" * 60)

    # 基本替换 + 反向引用
    text = "手机: 13812345678, 备用: 13998765432"
    masked = re.sub(r"(\d{3})\d{4}(\d{4})", r"\1****\2", text)
    print(f"  手机号脱敏: {masked}")

    # count 参数控制替换次数（类似 Java replaceFirst）
    result = re.sub(r"\d+", "X", "a1b2c3", count=1)
    print(f"  替换一次: {result}")       # aXb2c3
    # 用函数作为替换参数（Java 需要 Matcher.appendReplacement 循环）
    def double_number(match):
        return str(int(match.group()) * 2)

    result = re.sub(r"\d+", double_number, "苹果3个, 香蕉5个, 西瓜1个")
    print(f"  函数替换(翻倍): {result}")
    # subn 返回 (替换结果, 替换次数)
    result, n = re.subn(r"\d+", "#", "a1b2c3d4")
    print(f"  subn: '{result}', 替换了 {n} 次")


# =============================================================================
# 5. re.split
# =============================================================================

def split_demo():
    """
    正则分割 —— 对比 Java String.split(regex)
    """
    print("\n" + "=" * 60)
    print("5. re.split")
    print("=" * 60)

    # 基本分割
    result = re.split(r"[,;]\s*", "苹果, 香蕉;; 西瓜 , 葡萄")
    print(f"  基本分割: {result}")

    # maxsplit 控制分割次数
    result = re.split(r"\s+", "one two three four five", maxsplit=2)
    print(f"  限制次数: {result}")    # ['one', 'two', 'three four five']
    # 带分组的 split 会保留分隔符
    result = re.split(r"(\s*[,;]\s*)", "a, b; c")
    print(f"  保留分隔符: {result}")

    # 对比 str.split（不支持正则但更快）
    pattern = r"\s+"
    print(f"\n  str.split():  {'a b  c   d'.split()}")
    print(f"  re.split():   {re.split(pattern, 'a b  c   d')}")
    print(f"  (简单场景优先用 str.split，性能更好)")


# =============================================================================
# 6. re.compile 预编译
# =============================================================================

def compile_demo():
    """
    预编译正则 —— 对比 Java Pattern.compile()

    Java: private static final Pattern P = Pattern.compile("...");
    Python: P = re.compile(r"...")
    """
    print("\n" + "=" * 60)
    print("6. re.compile 预编译")
    print("=" * 60)

    # 预编译：解析一次，多次使用（循环中性能优势明显）
    email_re = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

    emails_text = "联系: zhang@example.com, li@test.org, admin@corp.com.cn, bad@"
    found = email_re.findall(emails_text)
    print(f"  pattern 对象: {email_re}")
    print(f"  找到的邮箱: {found}")
    # 编译后的对象拥有和 re 模块相同的方法
    print(f"\n  编译对象方法:")
    print(f"    .search()  = {email_re.search('test@x.com')}")
    print(f"    .findall() = {email_re.findall('a@b.c d@e.f')}")
    print(f"    .sub()     = {email_re.sub('[隐藏]', 'mail: test@x.com')}")
    # 性能：循环内反复使用 -> compile；偶尔用一次 -> 直接 re.search
    # re 模块内部缓存最近的 pattern（上限 512）


# =============================================================================
# 7. 常用正则模式（邮箱、手机号、IP）
# =============================================================================

def common_patterns_demo():
    """常用正则模式速查"""
    print("\n" + "=" * 60)
    print("7. 常用正则模式（邮箱、手机号、IP）")
    print("=" * 60)

    # 中国大陆手机号（1开头，第二位3-9，共11位）
    PHONE = re.compile(r"\b1[3-9]\d{9}\b")
    # 邮箱（简化版）
    EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    # IPv4 地址（精确匹配 0-255）
    IPV4 = re.compile(
        r"(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)"
    )
    # 身份证号（18位，最后一位可能是X）
    ID_CARD = re.compile(r"\b\d{17}[\dX]\b")

    test_data = """
    手机: 13812345678, 无效: 12345678901, 有效: 15999887766
    邮箱: test@example.com, admin@test.org, bad@, name+tag@mail.co.uk
    IP: 192.168.1.1, 10.0.0.255, 999.999.999.999, 172.16.0.1
    身份证: 110101199003071234, 440305198812120X, 12345
    """

    print(f"  手机号: {PHONE.findall(test_data)}")
    print(f"  邮箱:   {EMAIL.findall(test_data)}")
    print(f"  IPv4:   {IPV4.findall(test_data)}")
    print(f"  身份证: {ID_CARD.findall(test_data)}")


# =============================================================================
# 8. re.VERBOSE 可读正则
# =============================================================================

def verbose_demo():
    """
    用 re.VERBOSE 写可读的正则 —— 告别"天书"
    Java 对比: Pattern.compile("...", Pattern.COMMENTS)
    """
    print("\n" + "=" * 60)
    print("8. re.VERBOSE 可读正则")
    print("=" * 60)

    # 用 VERBOSE —— 可以加注释和换行，空白被忽略
    ipv4_pattern = re.compile(r"""
        ^
        (?:                                     # 前三段
            (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)  # 0-255
            \.                                  # 点号
        ){3}
        (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)   # 最后一段
        $
    """, re.VERBOSE)

    print("  VERBOSE 验证 IPv4:")
    for ip in ["192.168.1.1", "10.0.0.255", "256.1.1.1", "1.2.3.4"]:
        status = "valid" if ipv4_pattern.fullmatch(ip) else "invalid"
        print(f"    {ip:>15} -> {status}")

    # 组合多个标志位（用 | 运算符）
    url_pattern = re.compile(r"""
        (?P<protocol>https?)    # 协议
        ://                     # 分隔符
        (?P<host>[\w.-]+)       # 主机名
        (?::(?P<port>\d+))?     # 可选端口
        (?P<path>/\S*)?         # 可选路径
    """, re.VERBOSE | re.IGNORECASE)

    print(f"\n  VERBOSE + IGNORECASE 解析 URL:")
    for url in ["https://example.com/path", "HTTP://Test.Org:8080/api/v1"]:
        m = url_pattern.search(url)
        if m:
            d = m.groupdict()
            print(f"    {url}")
            print(f"      -> protocol={d['protocol']}, host={d['host']}, "
                  f"port={d['port']}, path={d['path']}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    match_search_fullmatch_demo()
    findall_finditer_demo()
    named_group_demo()
    sub_demo()
    split_demo()
    compile_demo()
    common_patterns_demo()
    verbose_demo()
