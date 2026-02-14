"""
Python3 多线程 —— 写给 Java 开发者

核心概念：
- Python 有 GIL（全局解释器锁），多线程不能利用多核做 CPU 密集任务
- 类比 Java: threading 模块类似 java.lang.Thread
- Python 多线程适合 IO 密集型任务，CPU 密集型请用多进程
"""

import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed


# =============================================================================
# 1. 创建线程 (threading.Thread)
#    Java 对比: new Thread(() -> { ... }).start()  /  implements Runnable
# =============================================================================

def thread_creation_demo():
    """创建线程的几种方式"""

    print("=" * 60)
    print("1. 创建线程")
    print("=" * 60)

    # --- 方式一：传入 target 函数 ---
    # Java: new Thread(() -> System.out.println("hello")).start();
    def worker(name, delay):
        print(f"  [线程 {name}] 开始"); time.sleep(delay); print(f"  [线程 {name}] 完成")

    t1 = threading.Thread(target=worker, args=("A", 0.1))
    t2 = threading.Thread(target=worker, args=("B", 0.05))
    t1.start(); t2.start()     # 类似 Java thread.start()
    t1.join();  t2.join()      # 类似 Java thread.join()
    print("  所有线程已完成\n")

    # --- 方式二：继承 Thread 类 ---
    # Java: class MyThread extends Thread { public void run() { ... } }
    class MyThread(threading.Thread):
        def __init__(self, name, delay):
            super().__init__()
            self.thread_name = name
            self.delay = delay

        def run(self):
            print(f"  [子类线程 {self.thread_name}] 开始")
            time.sleep(self.delay)
            print(f"  [子类线程 {self.thread_name}] 结束")

    t3 = MyThread("C", 0.05)
    t3.start()
    t3.join()

    # --- 获取线程信息 ---
    # Java: Thread.currentThread().getName()
    t = threading.current_thread()
    print(f"  当前线程: {t.name}, 活跃线程数: {threading.active_count()}")


# =============================================================================
# 2. GIL 的影响
#    Java 没有 GIL，多线程可以真正并行 CPU 密集任务
#    Python 的 GIL 使得同一时刻只有一个线程执行字节码
# =============================================================================

def gil_impact_demo():
    """演示 GIL 对 CPU 密集型任务的影响"""

    print("\n" + "=" * 60)
    print("2. GIL 的影响")
    print("=" * 60)

    def cpu_work(n):
        return sum(i * i for i in range(n))

    count = 500_000

    start = time.perf_counter()
    cpu_work(count); cpu_work(count)           # 单线程串行两次
    single_time = time.perf_counter() - start

    start = time.perf_counter()
    t1 = threading.Thread(target=cpu_work, args=(count,))
    t2 = threading.Thread(target=cpu_work, args=(count,))
    t1.start(); t2.start()                     # 双线程并发两次
    t1.join(); t2.join()
    multi_time = time.perf_counter() - start

    print(f"  单线程: {single_time:.4f}s | 双线程: {multi_time:.4f}s")
    print(f"  结论: 因为 GIL，双线程 CPU 密集任务并不更快！")
    print(f"  Java 没有 GIL，可以真正并行。Python CPU 密集型请用 multiprocessing。")


# =============================================================================
# 3. 线程池 (ThreadPoolExecutor)
#    Java 对比: ExecutorService pool = Executors.newFixedThreadPool(3);
# =============================================================================

def thread_pool_demo():
    """线程池的使用"""

    print("\n" + "=" * 60)
    print("3. 线程池 (ThreadPoolExecutor)")
    print("=" * 60)

    def fetch_url(url):
        """模拟网络请求"""
        time.sleep(0.05)
        return f"来自 {url} 的数据"

    urls = [f"https://api.example.com/{i}" for i in range(5)]

    # --- submit + as_completed ---
    # Java: Future<T> future = pool.submit(callable); future.get();
    print("\n  submit + as_completed:")
    with ThreadPoolExecutor(max_workers=3) as pool:
        future_map = {pool.submit(fetch_url, u): u for u in urls}
        for fut in as_completed(future_map):
            print(f"    {future_map[fut]} -> {fut.result()}")

    # --- map（更简洁，保持顺序） ---
    # Java: pool.invokeAll(tasks).stream().map(Future::get)
    print("\n  map（保持顺序）:")
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(fetch_url, urls):
            print(f"    {result}")

    # --- 异常处理 ---
    def risky_task(n):
        if n == 2:
            raise ValueError(f"任务 {n} 出错！")
        time.sleep(0.02)
        return f"任务 {n} 成功"

    print("\n  异常处理（Java: future.get() 抛 ExecutionException）:")
    with ThreadPoolExecutor(max_workers=2) as pool:
        futs = {pool.submit(risky_task, i): i for i in range(4)}
        for f in as_completed(futs):
            try:
                print(f"    任务 {futs[f]}: {f.result()}")
            except ValueError as e:
                print(f"    任务 {futs[f]} 异常: {e}")


# =============================================================================
# 4. 守护线程 (daemon thread)
#    Java 对比: thread.setDaemon(true);  // 必须在 start() 前
# =============================================================================

def daemon_thread_demo():
    """守护线程 —— 所有非守护线程结束后自动终止"""

    print("\n" + "=" * 60)
    print("4. 守护线程 (daemon)")
    print("=" * 60)

    def background_task():
        print("  [守护线程] 启动"); time.sleep(0.05); print("  [守护线程] 仍在运行...")

    def normal_task():
        print("  [普通线程] 启动"); time.sleep(0.03); print("  [普通线程] 完成")

    # daemon=True 类似 Java thread.setDaemon(true)
    daemon_t = threading.Thread(target=background_task, daemon=True)
    normal_t = threading.Thread(target=normal_task)
    daemon_t.start(); normal_t.start()
    print(f"  daemon_t.daemon={daemon_t.daemon}, normal_t.daemon={normal_t.daemon}")
    normal_t.join()
    daemon_t.join(timeout=0.1)
    print("  守护线程适合: 日志记录、心跳检测、缓存清理等后台任务")


# =============================================================================
# 5. 线程间通信 (Queue)
#    Java 对比: BlockingQueue<T> / LinkedBlockingQueue<T>
# =============================================================================

def thread_queue_demo():
    """使用 Queue 实现生产者-消费者模式"""

    print("\n" + "=" * 60)
    print("5. 线程间通信 (Queue)")
    print("=" * 60)

    # queue.Queue 是线程安全的，类似 Java BlockingQueue
    q = queue.Queue(maxsize=5)    # 有界队列，类似 ArrayBlockingQueue(5)
    results = []

    def producer(q, items):
        for item in items:
            q.put(item)           # 阻塞放入，类似 Java queue.put()
            print(f"  [生产者] 放入: {item}"); time.sleep(0.02)
        q.put(None)               # 毒丸模式（Poison Pill）通知消费者结束

    def consumer(q, results):
        while True:
            item = q.get()        # 阻塞取出，类似 Java queue.take()
            if item is None:      # 收到毒丸
                q.task_done(); break
            print(f"  [消费者] 处理: {item}")
            results.append(item.upper()); q.task_done()

    prod = threading.Thread(target=producer, args=(q, ["apple", "banana", "cherry"]))
    cons = threading.Thread(target=consumer, args=(q, results))
    prod.start(); cons.start()
    prod.join(); cons.join()
    print(f"  处理结果: {results}")

    # 非阻塞操作（类似 Java queue.poll()）+ Queue 变体
    q2 = queue.Queue()
    q2.put("test")
    print(f"  非阻塞取出: {q2.get_nowait()}")   # 空队列会抛 queue.Empty
    print("  变体: Queue(FIFO) / LifoQueue(栈) / PriorityQueue(优先级)")


# =============================================================================
# 6. threading.local() 线程本地存储
#    Java 对比: ThreadLocal<T>
# =============================================================================

def thread_local_demo():
    """每个线程拥有独立的变量副本"""

    print("\n" + "=" * 60)
    print("6. threading.local() 线程本地存储")
    print("=" * 60)

    # Java: ThreadLocal<String> ctx = new ThreadLocal<>();
    #       ctx.set("value"); ctx.get();
    local_data = threading.local()

    def process_request(user_name, request_id):
        local_data.user = user_name               # 类似 threadLocal.set()
        local_data.request_id = request_id
        time.sleep(0.02)
        # 读取时不会受其他线程影响（类似 threadLocal.get()）
        print(f"  [{threading.current_thread().name}] "
              f"user={local_data.user}, rid={local_data.request_id}")

    threads = [
        threading.Thread(target=process_request, args=(f"用户{i}", f"REQ-{i:03d}"),
                         name=f"Worker-{i}")
        for i in range(3)
    ]
    for t in threads: t.start()
    for t in threads: t.join()

    print("  典型用途: 数据库连接、用户会话、请求上下文（如 Flask request）")


# =============================================================================
# 7. 适用场景：IO 密集型任务
# =============================================================================

def io_bound_demo():
    """IO 密集型任务 —— 多线程的正确用法"""

    print("\n" + "=" * 60)
    print("7. 适用场景：IO 密集型任务")
    print("=" * 60)

    def simulated_io(task_name, duration):
        """模拟 IO 操作（GIL 在 IO 等待时释放，允许其他线程运行）"""
        time.sleep(duration)
        return f"{task_name} 完成"

    tasks = [
        ("数据库查询", 0.05), ("调用外部API", 0.08), ("读取文件", 0.03),
        ("发送邮件", 0.06),   ("写入日志", 0.02),
    ]

    # 串行执行
    start = time.perf_counter()
    for name, dur in tasks:
        simulated_io(name, dur)
    serial_time = time.perf_counter() - start
    print(f"  串行耗时: {serial_time:.4f}s")

    # 多线程并发
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(simulated_io, n, d) for n, d in tasks]
        for f in as_completed(futures):
            print(f"    {f.result()}")
    parallel_time = time.perf_counter() - start
    print(f"  并发耗时: {parallel_time:.4f}s, 加速比: {serial_time/parallel_time:.1f}x")

    # --- 总结对照表 ---
    table = [
        ("threading.Thread",              "java.lang.Thread"),
        ("ThreadPoolExecutor",            "ExecutorService"),
        ("queue.Queue",                   "BlockingQueue"),
        ("threading.local()",             "ThreadLocal<T>"),
        ("threading.Lock",               "synchronized / ReentrantLock"),
        ("有 GIL（CPU 密集不能并行）",     "无 GIL（真正并行）"),
        ("CPU 密集 -> multiprocessing",   "CPU 密集 -> 直接多线程"),
        ("IO 密集 -> threading",          "IO 密集 -> 多线程 / NIO"),
    ]
    print(f"\n  {'Python':<33}| Java")
    print(f"  {'-'*33}|{'-'*25}")
    for py, java in table:
        print(f"  {py:<33}| {java}")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    thread_creation_demo()
    gil_impact_demo()
    thread_pool_demo()
    daemon_thread_demo()
    thread_queue_demo()
    thread_local_demo()
    io_bound_demo()
