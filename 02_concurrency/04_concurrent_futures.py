"""
Python3 concurrent.futures —— 写给 Java 开发者

核心概念：
- concurrent.futures 是 Python 的高级并发接口
- 类比 Java: 几乎等同于 ExecutorService + Future
- 统一了线程池和进程池的 API
"""

import concurrent.futures
import time
import math
import random

# --- 进程池需要的函数必须定义在模块顶层（需要可 pickle 序列化）---

def _is_prime(n):
    """判断素数（CPU 密集型）"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def _compute_chunk(chunk):
    """计算一组数的阶乘之和"""
    return sum(math.factorial(n) for n in chunk)


# =============================================================================
# 1. ThreadPoolExecutor —— 对比 Java Executors.newFixedThreadPool
# =============================================================================

def thread_pool_demo():
    """线程池基础用法"""
    print("=" * 60)
    print("ThreadPoolExecutor（线程池）")
    print("=" * 60)

    # Java:  ExecutorService pool = Executors.newFixedThreadPool(3);
    #        pool.submit(() -> doWork());  pool.shutdown();
    # Python: with 语句自动调用 shutdown(wait=True)，类似 try-with-resources

    def download_page(url):
        time.sleep(random.uniform(0.1, 0.3))
        return f"  [{url}] 大小: {random.randint(1000, 9999)} bytes"

    urls = [f"https://example.com/page{i}" for i in range(1, 5)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(download_page, url) for url in urls]
        for future in futures:
            print(future.result())  # 阻塞等待，类似 Java future.get()
    print("  线程池已自动关闭（shutdown）")


# =============================================================================
# 2. ProcessPoolExecutor —— 对比 Java ForkJoinPool
# =============================================================================

def process_pool_demo():
    """进程池：适合 CPU 密集型任务（绕过 GIL）"""
    print("\n" + "=" * 60)
    print("ProcessPoolExecutor（进程池）")
    print("=" * 60)

    # 只需把 ThreadPoolExecutor 换成 ProcessPoolExecutor，API 完全一致！
    # 注意：传给进程池的函数必须定义在模块顶层（需要可 pickle 序列化）
    numbers = [112272535095293, 112582705942171, 115280095190773, 115797848077099]

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(_is_prime, numbers))
    parallel = time.perf_counter() - start

    for num, prime in zip(numbers, results):
        print(f"  {num} 是素数: {prime}")
    print(f"  进程池耗时: {parallel:.3f}s")

    start = time.perf_counter()
    [_is_prime(n) for n in numbers]
    serial = time.perf_counter() - start
    print(f"  串行耗时:   {serial:.3f}s")


# =============================================================================
# 3. Future 对象 —— 对比 Java Future / CompletableFuture
# =============================================================================

def future_demo():
    """Future 对象的方法"""
    print("\n" + "=" * 60)
    print("Future 对象")
    print("=" * 60)

    # Java Future 方法          Python Future 方法
    # future.get()           -> future.result()
    # future.get(timeout)    -> future.result(timeout=5)
    # future.isDone()        -> future.done()
    # future.cancel()        -> future.cancel()
    # future.isCancelled()   -> future.cancelled()
    # （无）                 -> future.add_done_callback(fn)  类似 CompletableFuture
    # （无）                 -> future.exception()            获取异常对象

    def slow_task(name, seconds):
        time.sleep(seconds)
        return f"{name} 完成"

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(slow_task, "任务A", 0.2)
        print(f"  提交后立即检查 done(): {future.done()}")
        print(f"  result (阻塞等待): {future.result()}")
        print(f"  完成后检查 done():   {future.done()}")

        # add_done_callback —— 回调，类似 CompletableFuture.thenAccept
        def on_complete(f):
            print(f"  [回调] 任务完成，结果: {f.result()}")

        future2 = executor.submit(slow_task, "任务B", 0.1)
        future2.add_done_callback(on_complete)
        time.sleep(0.3)


# =============================================================================
# 4. submit() vs map()
# =============================================================================

def submit_vs_map_demo():
    """submit 和 map 的区别"""
    print("\n" + "=" * 60)
    print("submit() vs map()")
    print("=" * 60)

    def process(item):
        time.sleep(random.uniform(0.05, 0.15))
        return item * 10

    items = [1, 2, 3, 4, 5]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # map(): 按提交顺序返回结果（类似 Java parallelStream）
        print("--- map(): 结果按顺序返回 ---")
        for item, result in zip(items, executor.map(process, items)):
            print(f"  {item} -> {result}")

        # submit(): 返回 Future，配合 as_completed 按完成顺序处理
        print("\n--- submit(): 返回 Future 对象 ---")
        futures = {executor.submit(process, item): item for item in items}
        for future in concurrent.futures.as_completed(futures):
            original = futures[future]
            print(f"  {original} -> {future.result()} (按完成顺序)")

    # map()   - 简洁，按顺序返回，适合批量同构任务
    # submit() - 灵活，可以提交不同函数，可单独处理异常


# =============================================================================
# 5. as_completed() —— 获取最先完成的结果
# =============================================================================

def as_completed_demo():
    """as_completed: 哪个先完成就先处理哪个"""
    print("\n" + "=" * 60)
    print("as_completed() —— 先完成先处理")
    print("=" * 60)

    # Java 中类似 CompletionService.take()
    def fetch_data(source, delay):
        time.sleep(delay)
        return f"{source}: 数据就绪 (耗时 {delay}s)"

    tasks = [("数据库", 0.3), ("缓存", 0.05), ("远程API", 0.2)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_source = {
            executor.submit(fetch_data, src, d): src for src, d in tasks
        }
        for i, future in enumerate(
            concurrent.futures.as_completed(future_to_source), 1
        ):
            print(f"  第{i}个完成 -> {future.result()}")


# =============================================================================
# 6. wait() —— 等待多个 Future
# =============================================================================

def wait_demo():
    """wait: 更细粒度的等待控制"""
    print("\n" + "=" * 60)
    print("wait() —— 等待多个 Future")
    print("=" * 60)

    def task(name, seconds):
        time.sleep(seconds)
        return f"{name} 完成"

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(task, "快速任务", 0.05),
            executor.submit(task, "中速任务", 0.15),
            executor.submit(task, "慢速任务", 0.3),
        ]

        # FIRST_COMPLETED: 任一完成就返回（类似 Java invokeAny 的思路）
        done, not_done = concurrent.futures.wait(
            futures, return_when=concurrent.futures.FIRST_COMPLETED
        )
        print(f"  FIRST_COMPLETED: {len(done)} 完成, {len(not_done)} 未完成")
        for f in done:
            print(f"    -> {f.result()}")

        # ALL_COMPLETED: 全部完成（默认行为）
        done, not_done = concurrent.futures.wait(
            futures, return_when=concurrent.futures.ALL_COMPLETED
        )
        print(f"  ALL_COMPLETED:   {len(done)} 完成, {len(not_done)} 未完成")


# =============================================================================
# 7. 异常处理
# =============================================================================

def exception_handling_demo():
    """Future 中的异常处理"""
    print("\n" + "=" * 60)
    print("异常处理")
    print("=" * 60)

    # Java: future.get() 抛出 ExecutionException，需要 getCause()
    # Python: future.result() 直接抛出原始异常，更直观
    def risky_task(n):
        if n == 0:
            raise ValueError("不能为零！")
        if n < 0:
            raise TypeError("不能为负数！")
        return 100 / n

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 方式一：try/except 捕获
        futures = {executor.submit(risky_task, n): n for n in [10, 0, -1, 5]}
        for future in concurrent.futures.as_completed(futures):
            n = futures[future]
            try:
                result = future.result()
                print(f"  risky_task({n}) = {result}")
            except Exception as e:
                print(f"  risky_task({n}) 抛出 {type(e).__name__}: {e}")

        # 方式二：用 future.exception() 检查（不会抛出异常）
        print("\n--- 用 exception() 检查 ---")
        f = executor.submit(risky_task, 0)
        concurrent.futures.wait([f])
        err = f.exception()
        if err:
            print(f"  异常对象: {type(err).__name__}: {err}")
        else:
            print(f"  结果: {f.result()}")


# =============================================================================
# 8. 实际应用：批量下载、并行计算
# =============================================================================

def practical_demo():
    """综合实战示例"""
    print("\n" + "=" * 60)
    print("实际应用：批量下载 + 并行计算")
    print("=" * 60)

    # --- 批量下载（IO 密集型 -> 线程池）---
    print("--- 批量下载模拟（线程池）---")

    def download(url):
        time.sleep(random.uniform(0.05, 0.2))
        return {"url": url, "size": random.randint(500, 5000), "status": 200}

    urls = [f"https://api.example.com/data/{i}" for i in range(8)]
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(download, urls))
    elapsed = time.perf_counter() - start
    total_size = sum(r["size"] for r in results)
    print(f"  下载 {len(urls)} 个资源, 总大小: {total_size} bytes")
    print(f"  并发耗时: {elapsed:.3f}s")

    # --- 并行计算（CPU 密集型 -> 进程池）---
    print("\n--- 并行计算模拟（进程池）---")
    data = list(range(100, 140))
    chunk_size = 10
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        partial_sums = list(executor.map(_compute_chunk, chunks))
    total = sum(partial_sums)
    elapsed = time.perf_counter() - start
    print(f"  计算 {len(data)} 个数的阶乘之和")
    print(f"  分为 {len(chunks)} 个分片, 每片 {chunk_size} 个")
    print(f"  结果位数: {len(str(total))}")
    print(f"  并行耗时: {elapsed:.3f}s")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    thread_pool_demo()
    process_pool_demo()
    future_demo()
    submit_vs_map_demo()
    as_completed_demo()
    wait_demo()
    exception_handling_demo()
    practical_demo()
