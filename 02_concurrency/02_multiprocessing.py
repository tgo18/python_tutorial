"""
Python3 多进程 —— 写给 Java 开发者

核心概念：
- 多进程是 Python 突破 GIL 限制、利用多核的主要方式
- 类比 Java: multiprocessing 弥补了 Python 线程不能真并行的缺陷
- 每个进程有独立的 GIL，可以真正并行执行
"""

import multiprocessing as mp
import os
import time
import threading
from multiprocessing import Process, Pool, Queue, Pipe, Value, Array, Manager

# -- 辅助函数（必须在模块顶层定义，子进程需要 pickle 序列化）--

def _worker(name, count):
    for i in range(count):
        print(f"  [{name} PID={os.getpid()}] 工作中... {i + 1}/{count}")

def _square(x):          return x * x
def _square_info(x):     return (x, x * x, os.getpid())
def _process_item(x):    return x ** 2 + 1
def _process_pair(x, y): return x * y
def _update_dict(d, k, v): d[k] = v
def _append_list(lst, v):  lst.append(v)

def _producer(queue, items):
    for item in items:
        queue.put(item)
        print(f"  [生产者 PID={os.getpid()}] 放入: {item}")
    queue.put(None)  # 哨兵值

def _pipe_child(conn):
    conn.send(f"来自子进程 PID={os.getpid()} 的问候")
    print(f"  [子进程] 收到: {conn.recv()}")
    conn.close()

def _increment(shared_val, lock, n):
    for _ in range(n):
        with lock:
            shared_val.value += 1

def _fill_array(arr, start, count):
    for i in range(count):
        if start + i < len(arr):
            arr[start + i] = (start + i) * 10

def _cpu_work(n):
    return sum(i * i for i in range(n))

def _transform(record):
    name, score = record
    return {"name": name, "score": score, "bonus": sum(range(100))}


# =============================================================================
# 1. 创建进程 (multiprocessing.Process)
#    Java 对比: ProcessBuilder / new Thread() 但运行在独立进程
# =============================================================================

def process_creation_demo():
    """创建进程的基本方式"""
    print("=" * 60)
    print("1. 创建进程 (Process)")
    print("=" * 60)

    # Java: Thread t = new Thread(runnable); t.start();  但这里是独立进程
    print(f"  主进程 PID: {os.getpid()}")

    p1 = Process(target=_worker, args=("进程A", 2))
    p2 = Process(target=_worker, args=("进程B", 2))
    p1.start()  # 类似 Java Thread.start()
    p2.start()
    p1.join()   # 类似 Java Thread.join()
    p2.join()
    print(f"  p1 exitcode: {p1.exitcode}, p2 exitcode: {p2.exitcode}")

    # --- 继承 Process 类（类似 Java extends Thread）---
    class MyProcess(Process):
        def __init__(self, label):
            super().__init__()
            self.label = label
        def run(self):
            print(f"  [子类进程 {self.label}] PID={os.getpid()}")

    p3 = MyProcess("自定义")
    p3.start()
    p3.join()
    print(f"  所有进程已结束")


# =============================================================================
# 2. 进程池 (Pool)
#    Java 对比: ExecutorService / ThreadPoolExecutor
# =============================================================================

def pool_demo():
    """进程池的使用"""
    print("\n" + "=" * 60)
    print("2. 进程池 (Pool)")
    print("=" * 60)

    # Java: ExecutorService pool = Executors.newFixedThreadPool(4);
    with Pool(processes=2) as pool:
        # 同步调用（阻塞等结果）
        print(f"  apply 同步: {pool.apply(_square, args=(10,))}")
        # 异步调用（类似 Java Future）
        future = pool.apply_async(_square, args=(20,))
        print(f"  apply_async: {future.get(timeout=5)}")

    # with Pool 等价于 Java try-with-resources + ExecutorService
    with Pool(processes=2) as pool:
        results = pool.map(_square_info, range(6))
        print(f"\n  Pool.map 结果:")
        pids = set()
        for val, sq, pid in results:
            pids.add(pid)
            print(f"    {val}^2 = {sq}  (PID={pid})")
        print(f"  使用了 {len(pids)} 个工作进程")


# =============================================================================
# 3. 进程间通信 (Queue, Pipe)
#    Java 对比: BlockingQueue / PipedInputStream
# =============================================================================

def ipc_demo():
    """进程间通信演示"""
    print("\n" + "=" * 60)
    print("3. 进程间通信 (Queue, Pipe)")
    print("=" * 60)

    # --- Queue（类似 Java BlockingQueue）---
    print("--- Queue 通信 ---")
    queue = Queue()
    p = Process(target=_producer, args=(queue, [1, 2, 3]))
    p.start()
    p.join()
    while not queue.empty():
        item = queue.get()
        if item is not None:
            print(f"  [主进程] 取出: {item}")

    # --- Pipe（双向通信，类似 Java PipedStream）---
    print("\n--- Pipe 通信 ---")
    parent_conn, child_conn = Pipe()
    p = Process(target=_pipe_child, args=(child_conn,))
    p.start()
    print(f"  [主进程] 收到: {parent_conn.recv()}")
    parent_conn.send("主进程已收到，谢谢！")
    p.join()


# =============================================================================
# 4. 共享内存 (Value, Array, Manager)
#    Java 对比: AtomicInteger / ConcurrentHashMap
# =============================================================================

def shared_memory_demo():
    """共享内存演示"""
    print("\n" + "=" * 60)
    print("4. 共享内存 (Value, Array, Manager)")
    print("=" * 60)

    # --- Value（类似 Java AtomicInteger，'i'=int, 'd'=double）---
    print("--- Value 共享变量 ---")
    counter, lock = Value('i', 0), mp.Lock()
    procs = [Process(target=_increment, args=(counter, lock, 100)) for _ in range(4)]
    for p in procs: p.start()
    for p in procs: p.join()
    print(f"  4 个进程各加 100 次，最终值: {counter.value}")  # 应为 400

    # --- Array（共享数组）---
    print("\n--- Array 共享数组 ---")
    arr = Array('i', 8)
    p1 = Process(target=_fill_array, args=(arr, 0, 4))
    p2 = Process(target=_fill_array, args=(arr, 4, 4))
    p1.start(); p2.start()
    p1.join();  p2.join()
    print(f"  共享数组: {list(arr)}")

    # --- Manager（复杂共享数据，通过代理进程实现）---
    print("\n--- Manager 共享复杂对象 ---")
    with Manager() as mgr:
        d, lst = mgr.dict(), mgr.list()
        procs = [
            Process(target=_update_dict, args=(d, "a", 1)),
            Process(target=_update_dict, args=(d, "b", 2)),
            Process(target=_append_list, args=(lst, "x")),
            Process(target=_append_list, args=(lst, "y")),
        ]
        for p in procs: p.start()
        for p in procs: p.join()
        print(f"  共享字典: {dict(d)}")
        print(f"  共享列表: {list(lst)}")


# =============================================================================
# 5. map/starmap 并行处理
#    Java 对比: list.parallelStream().map(...)
# =============================================================================

def map_starmap_demo():
    """map/starmap 并行处理演示"""
    print("\n" + "=" * 60)
    print("5. map/starmap 并行处理")
    print("=" * 60)

    data = list(range(10))

    # Pool.map — Java: data.parallelStream().map(fn).collect(toList())
    print("--- Pool.map ---")
    with Pool(processes=2) as pool:
        results = pool.map(_process_item, data)
    print(f"  输入: {data}")
    print(f"  输出: {results}")

    # Pool.starmap — 多参数版 map（Java 无直接对应）
    print("\n--- Pool.starmap（多参数）---")
    pairs = [(1, 10), (2, 20), (3, 30), (4, 40)]
    with Pool(processes=2) as pool:
        results = pool.starmap(_process_pair, pairs)
    print(f"  参数对: {pairs}")
    print(f"  结果:   {results}")

    # imap — 惰性迭代器（类似 Java Stream 的惰性求值）
    print("\n--- Pool.imap（惰性迭代）---")
    with Pool(processes=2) as pool:
        for r in pool.imap(_process_item, range(6)):
            print(f"    -> {r}", end="")
    print()


# =============================================================================
# 6. GIL 对比：多线程 vs 多进程性能差异
#    核心要点：CPU 密集型任务中多进程远快于多线程
# =============================================================================

def gil_comparison_demo():
    """GIL 对多线程 vs 多进程的影响"""
    print("\n" + "=" * 60)
    print("6. GIL 对比: 多线程 vs 多进程")
    print("=" * 60)

    # Java 无 GIL，多线程可真并行；Python 必须靠多进程突破 GIL
    work_size, num_workers = 500_000, 4

    # 串行
    t0 = time.perf_counter()
    for _ in range(num_workers): _cpu_work(work_size)
    serial = time.perf_counter() - t0
    print(f"  串行执行: {serial:.3f}s")

    # 多线程（受 GIL 限制）
    t0 = time.perf_counter()
    threads = [threading.Thread(target=_cpu_work, args=(work_size,))
               for _ in range(num_workers)]
    for t in threads: t.start()
    for t in threads: t.join()
    t_time = time.perf_counter() - t0
    print(f"  多线程:   {t_time:.3f}s (受 GIL 限制)")

    # 多进程（突破 GIL）
    t0 = time.perf_counter()
    with Pool(processes=num_workers) as pool:
        pool.map(_cpu_work, [work_size] * num_workers)
    p_time = time.perf_counter() - t0
    print(f"  多进程:   {p_time:.3f}s (真正并行)")

    print(f"\n  结论:")
    print(f"    多线程 vs 串行: {t_time / serial:.2f}x")
    print(f"    多进程 vs 串行: {p_time / serial:.2f}x")
    print(f"    CPU 密集型任务应使用多进程!")


# =============================================================================
# 7. 适用场景：CPU 密集型任务
#    CPU 密集型 -> 多进程; IO 密集型 -> 多线程/协程
# =============================================================================

def use_case_demo():
    """适用场景演示"""
    print("\n" + "=" * 60)
    print("7. 适用场景：CPU 密集型任务")
    print("=" * 60)

    # Java 可以用多线程处理 CPU 密集型，Python 必须用多进程
    print("""
  Python 并发选择指南（对比 Java）:
  ┌─────────────┬──────────────────┬──────────────────────┐
  │ 任务类型     │ Python 推荐       │ Java 对应             │
  ├─────────────┼──────────────────┼──────────────────────┤
  │ CPU 密集型   │ multiprocessing   │ Thread / ForkJoinPool │
  │ IO 密集型    │ threading/asyncio │ Thread / CompleteFuture│
  │ 混合型       │ Process + Thread  │ ThreadPool            │
  └─────────────┴──────────────────┴──────────────────────┘
  multiprocessing 典型应用:
  - 数值计算、图像/视频处理、数据 ETL、ML 数据预处理""")

    # --- 实际示例：并行批量处理 ---
    print("\n--- 实际示例：并行批量处理 ---")
    records = [(f"user_{i}", i * 10) for i in range(8)]
    with Pool(processes=2) as pool:
        results = pool.map(_transform, records)
    for r in results[:3]:
        print(f"    {r}")
    print(f"    ... 共处理 {len(results)} 条记录")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    process_creation_demo()
    pool_demo()
    ipc_demo()
    shared_memory_demo()
    map_starmap_demo()
    gil_comparison_demo()
    use_case_demo()
