"""
Python3 日期与时间 —— 写给 Java 开发者

核心概念：
- datetime 模块是 Python 处理日期时间的标准库
- 类比 Java: datetime ≈ java.time (LocalDateTime/ZonedDateTime/Instant)
- Python 3.9+ 用 zoneinfo 处理时区，告别第三方 pytz
"""

from datetime import date, time, datetime, timedelta, timezone
import calendar

try:
    from zoneinfo import ZoneInfo          # Python 3.9+
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore


# ============================================================
# 1. date, time, datetime 对象
#    Java 对比: LocalDate, LocalTime, LocalDateTime
# ============================================================

def date_time_objects_demo():
    """date / time / datetime 三大核心类"""

    print("=" * 60)
    print("1. date, time, datetime 对象")
    print("=" * 60)

    # date: 只有日期 (Java: LocalDate.of(2025, 6, 15))
    d = date(2025, 6, 15)
    print(f"date: {d}  year={d.year}, month={d.month}, day={d.day}")
    print(f"  weekday={d.weekday()} (0=周一)  isoweekday={d.isoweekday()} (1=周一)")

    # time: 只有时间 (Java: LocalTime.of(14, 30, 45))
    t = time(14, 30, 45, 123456)       # 时, 分, 秒, 微秒
    print(f"time: {t}  microsecond={t.microsecond}")  # Java 用 getNano()

    # datetime: 日期+时间 (Java: LocalDateTime.of(...))
    dt = datetime(2025, 6, 15, 14, 30, 45)
    print(f"datetime: {dt}  date()={dt.date()}, time()={dt.time()}")

    # 组合 (Java: LocalDateTime.of(localDate, localTime))
    print(f"  combine: {datetime.combine(d, time(9, 0))}")


# ============================================================
# 2. 创建日期时间 (now, today, 构造函数)
# ============================================================

def creation_demo():
    """创建日期时间的多种方式"""

    print("\n" + "=" * 60)
    print("2. 创建日期时间")
    print("=" * 60)

    # Java: LocalDate.now() / LocalDateTime.now()
    print(f"date.today()      = {date.today()}")
    print(f"datetime.now()    = {datetime.now()}")
    print(f"datetime.now(utc) = {datetime.now(timezone.utc)}")

    # 构造函数 (Java: LocalDateTime.of(year, month, ...))
    dt = datetime(2025, 1, 1, 0, 0, 0)
    print(f"构造函数: {dt}")

    # replace 返回新对象 (Java: localDateTime.withYear(2026))
    print(f"replace:  {dt.replace(year=2026, month=6)}  (原对象不变: {dt})")


# ============================================================
# 3. 日期时间运算 (timedelta)
#    Java 对比: Duration（时间段） / Period（日期段）
# ============================================================

def timedelta_demo():
    """日期时间运算"""

    print("\n" + "=" * 60)
    print("3. 日期时间运算 (timedelta)")
    print("=" * 60)

    now = datetime(2025, 6, 15, 10, 0, 0)

    # 创建时间差 (Java: Duration.ofHours(3) / Period.ofDays(7))
    print(f"当前: {now}")
    print(f"  +1小时: {now + timedelta(hours=1)}")
    print(f"  +7天:   {now + timedelta(days=7)}")
    print(f"  -3天:   {now - timedelta(days=3)}")

    delta = timedelta(weeks=2, days=3, hours=5, minutes=30)
    print(f"  复合: {delta} = {delta.total_seconds()}秒")

    # 两个日期相减 (Java: Duration.between(start, end))
    diff = datetime(2025, 12, 25) - now
    print(f"\n距圣诞节: {diff.days}天, 总秒数={diff.total_seconds()}")

    # 比较 (Java: d1.isBefore(d2))
    d1, d2 = date(2025, 1, 1), date(2025, 12, 31)
    print(f"{d1} < {d2}: {d1 < d2}")

    print("\n注意: timedelta 没有 '月/年'，需要 dateutil.relativedelta")


# ============================================================
# 4. 格式化 strftime
#    Java 对比: DateTimeFormatter.ofPattern("yyyy-MM-dd")
# ============================================================

def strftime_demo():
    """日期时间格式化"""

    print("\n" + "=" * 60)
    print("4. 格式化 strftime")
    print("=" * 60)

    # Java: DateTimeFormatter fmt = DateTimeFormatter.ofPattern("...");
    #       String s = localDateTime.format(fmt);
    dt = datetime(2025, 6, 15, 14, 30, 45)
    print(f"原始: {dt}")
    print(f"  %Y-%m-%d %H:%M:%S -> {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  %Y年%m月%d日      -> {dt.strftime('%Y年%m月%d日')}")
    print(f"  %A %p             -> {dt.strftime('%A %p')}")

    # 符号速查 (Python vs Java)
    print("\n  Python | Java   | 含义")
    print("  -------|--------|--------")
    for py, jv, desc in [
        ("%Y", "yyyy", "四位年"), ("%m", "MM", "两位月"),
        ("%d", "dd", "两位日"),   ("%H", "HH", "24小时"),
        ("%I", "hh", "12小时"),   ("%M", "mm", "分钟"),
        ("%S", "ss", "秒"),       ("%f", "SSSSSS", "微秒"),
        ("%A", "EEEE", "星期"),   ("%p", "a", "AM/PM"),
    ]:
        print(f"  {py:6s} | {jv:6s} | {desc}")


# ============================================================
# 5. 解析 strptime
#    Java 对比: LocalDateTime.parse(str, DateTimeFormatter)
# ============================================================

def strptime_demo():
    """字符串解析为日期时间"""

    print("\n" + "=" * 60)
    print("5. 解析 strptime")
    print("=" * 60)

    # strptime = "string parse time"
    for s, fmt in [
        ("2025-06-15 14:30:45", "%Y-%m-%d %H:%M:%S"),
        ("2025年06月15日",       "%Y年%m月%d日"),
        ("15/06/2025 02:30 PM", "%d/%m/%Y %I:%M %p"),
    ]:
        dt = datetime.strptime(s, fmt)
        print(f"  '{s}' -> {dt}")

    print("\n  记忆: strftime = format time (对象->字符串)")
    print("        strptime = parse time  (字符串->对象)")


# ============================================================
# 6. 时间戳互转
#    Java 对比: Instant.toEpochMilli() / Instant.ofEpochMilli()
# ============================================================

def timestamp_demo():
    """时间戳与 datetime 互转"""

    print("\n" + "=" * 60)
    print("6. 时间戳互转")
    print("=" * 60)

    import time as time_mod

    # datetime -> 时间戳 (Java: instant.toEpochMilli() / 1000)
    dt = datetime(2025, 6, 15, 14, 30, 45)
    ts = dt.timestamp()
    print(f"datetime -> 时间戳: {dt} -> {ts}")
    print(f"  Python 返回秒(float)，Java 通常用毫秒(long)")

    # 时间戳 -> datetime (Java: Instant.ofEpochSecond(ts))
    print(f"时间戳 -> datetime: {datetime.fromtimestamp(ts)}")
    print(f"时间戳 -> UTC:      {datetime.fromtimestamp(ts, tz=timezone.utc)}")
    print(f"当前时间戳: {time_mod.time()}")

    # Java 毫秒时间戳 (System.currentTimeMillis())
    java_ms = 1750000000000
    print(f"\nJava 毫秒 {java_ms} -> {datetime.fromtimestamp(java_ms / 1000)}")
    print("  技巧: Java毫秒 / 1000 = Python秒")


# ============================================================
# 7. 时区处理 (zoneinfo.ZoneInfo, Python 3.9+)
#    Java 对比: ZoneId / ZonedDateTime
# ============================================================

def timezone_demo():
    """时区处理"""

    print("\n" + "=" * 60)
    print("7. 时区处理 (zoneinfo)")
    print("=" * 60)

    # Java: ZoneId.of("Asia/Shanghai"); ZonedDateTime.now(zoneId)
    shanghai = ZoneInfo("Asia/Shanghai")
    tokyo = ZoneInfo("Asia/Tokyo")
    ny = ZoneInfo("America/New_York")

    print(f"上海: {datetime.now(shanghai)}")
    print(f"东京: {datetime.now(tokyo)}")
    print(f"纽约: {datetime.now(ny)}")

    # naive vs aware (LocalDateTime vs ZonedDateTime)
    naive_dt = datetime(2025, 6, 15, 10, 0, 0)
    aware_dt = datetime(2025, 6, 15, 10, 0, 0, tzinfo=shanghai)

    print(f"\nnaive: {naive_dt}, tzinfo={naive_dt.tzinfo}")
    print(f"aware: {aware_dt}, tzinfo={aware_dt.tzinfo}")
    print("  警告: naive 和 aware 不能直接比较 (TypeError)")


# ============================================================
# 8. UTC 与本地时间转换
# ============================================================

def utc_conversion_demo():
    """UTC 与本地时间转换"""

    print("\n" + "=" * 60)
    print("8. UTC 与本地时间转换")
    print("=" * 60)

    shanghai = ZoneInfo("Asia/Shanghai")

    # UTC -> 本地 (Java: utcTime.withZoneSameInstant(zoneId))
    utc_time = datetime(2025, 6, 15, 6, 0, 0, tzinfo=timezone.utc)
    local_time = utc_time.astimezone(shanghai)
    print(f"UTC {utc_time}")
    print(f" -> 上海 {local_time}")
    print(f" -> 转回 UTC {local_time.astimezone(timezone.utc)}")

    # 给 naive 添加时区 (Java: localDateTime.atZone(zoneId))
    naive = datetime(2025, 6, 15, 14, 0, 0)
    aware = naive.replace(tzinfo=shanghai)
    print(f"\nnaive->aware: {aware}  -> UTC: {aware.astimezone(timezone.utc)}")
    print(f"  UTC偏移: {local_time.utcoffset()}, 时区名: {local_time.tzname()}")


# ============================================================
# 9. ISO 格式 (isoformat, fromisoformat)
# ============================================================

def iso_format_demo():
    """ISO 8601 格式处理"""

    print("\n" + "=" * 60)
    print("9. ISO 格式")
    print("=" * 60)

    # Java: LocalDateTime.toString() 就是 ISO 格式
    dt = datetime(2025, 6, 15, 14, 30, 45)
    shanghai = ZoneInfo("Asia/Shanghai")

    aware_dt = dt.replace(tzinfo=shanghai)
    print(f"isoformat():   {dt.isoformat()}")
    print(f"带时区:        {aware_dt.isoformat()}")
    print(f"UTC:           {aware_dt.astimezone(timezone.utc).isoformat()}")

    # 解析 ISO (Java: LocalDateTime.parse("..."))
    for s in ["2025-06-15T14:30:45", "2025-06-15T14:30:45+08:00", "2025-06-15"]:
        print(f"  parse '{s}' -> {datetime.fromisoformat(s) if 'T' in s else date.fromisoformat(s)}")
    print("  注: Python 3.11+ 支持 'Z' 后缀，低版本用 '+00:00'")


# ============================================================
# 10. calendar 模块简介
# ============================================================

def calendar_demo():
    """calendar 模块"""

    print("\n" + "=" * 60)
    print("10. calendar 模块简介")
    print("=" * 60)

    # 月历
    print("2025年6月:")
    print(calendar.month(2025, 6))

    # 闰年 (Java: Year.isLeap(2024))
    print(f"2024 闰年: {calendar.isleap(2024)},  2025 闰年: {calendar.isleap(2025)}")

    # 某月天数 (Java: YearMonth.of(2025, 2).lengthOfMonth())
    wd, days = calendar.monthrange(2025, 2)
    print(f"2025年2月: 首日星期{wd}(0=周一), 共{days}天")
    wd, days = calendar.monthrange(2024, 2)
    print(f"2024年2月: 首日星期{wd}(0=周一), 共{days}天 (闰年)")


# ============================================================
# 11. 实际场景
# ============================================================

def practical_scenarios():
    """实际开发中的常见场景"""

    print("\n" + "=" * 60)
    print("11. 实际场景")
    print("=" * 60)

    # --- 场景一：时间戳转可读时间 ---
    print("\n--- 场景一：时间戳转可读时间 ---")

    def ts_to_readable(ts, tz_name="Asia/Shanghai"):
        dt = datetime.fromtimestamp(ts, tz=ZoneInfo(tz_name))
        return dt.strftime("%Y年%m月%d日 %H:%M:%S (%A)")

    sample_ts = 1750000000
    print(f"  {sample_ts} -> {ts_to_readable(sample_ts)}")
    print(f"  {sample_ts} (UTC) -> {ts_to_readable(sample_ts, 'UTC')}")

    # --- 场景二：跨时区会议时间转换 ---
    print("\n--- 场景二：跨时区会议时间转换 ---")

    def convert_meeting(dt_str, from_tz, to_tzs):
        src = ZoneInfo(from_tz)
        dt = datetime.fromisoformat(dt_str).replace(tzinfo=src)
        print(f"  原始 ({from_tz}): {dt.strftime('%Y-%m-%d %H:%M %Z')}")
        for tz_name in to_tzs:
            c = dt.astimezone(ZoneInfo(tz_name))
            print(f"    -> {tz_name}: {c.strftime('%Y-%m-%d %H:%M %Z')}")

    convert_meeting("2025-06-15T15:00:00", "Asia/Shanghai",
                     ["America/New_York", "Europe/London", "Asia/Tokyo"])

    # --- 场景三：计算工作日 ---
    print("\n--- 场景三：计算工作日 ---")

    def count_workdays(start, end):
        """weekday() < 5 即工作日（0=周一 ~ 4=周五）"""
        days = 0
        cur = start
        while cur <= end:
            if cur.weekday() < 5:
                days += 1
            cur += timedelta(days=1)
        return days

    def add_workdays(start, n):
        cur, added = start, 0
        while added < n:
            cur += timedelta(days=1)
            if cur.weekday() < 5:
                added += 1
        return cur

    wd = count_workdays(date(2025, 6, 1), date(2025, 6, 30))
    print(f"  2025年6月: 30天, 工作日{wd}天")
    print(f"  2025-06-15 + 10个工作日 = {add_workdays(date(2025, 6, 15), 10)}")

    # --- 总结对照表 ---
    print("\n" + "-" * 60)
    print("Python datetime vs Java java.time 对照表:")
    print("-" * 60)
    for py, jv in [
        ("date",                      "LocalDate"),
        ("time",                      "LocalTime"),
        ("datetime (naive)",          "LocalDateTime"),
        ("datetime (aware)",          "ZonedDateTime"),
        ("timedelta",                 "Duration / Period"),
        ("timezone.utc",              "ZoneOffset.UTC"),
        ("ZoneInfo('Asia/Shanghai')", "ZoneId.of('Asia/Shanghai')"),
        ("dt.timestamp()",            "instant.getEpochSecond()"),
        ("datetime.fromtimestamp()",  "Instant.ofEpochSecond()"),
        ("strftime / strptime",       "DateTimeFormatter"),
        ("dt.isoformat()",            "dt.toString()"),
        ("fromisoformat(s)",          "LocalDateTime.parse(s)"),
    ]:
        print(f"  {py:<30s} | {jv}")


# ============================================================
# 运行所有 demo
# ============================================================

if __name__ == "__main__":
    date_time_objects_demo()
    creation_demo()
    timedelta_demo()
    strftime_demo()
    strptime_demo()
    timestamp_demo()
    timezone_demo()
    utc_conversion_demo()
    iso_format_demo()
    calendar_demo()
    practical_scenarios()
