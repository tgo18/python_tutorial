"""
Python3 同步原语 —— 写给 Java 开发者

核心概念：
- Python 的同步原语和 Java 的 java.util.concurrent 高度相似
- 类比 Java: Lock, Condition, Semaphore, Barrier 概念一一对应
- Python 的 with 语句让锁的使用比 Java 更安全优雅
"""

import threading
import time


def _run_threads(*threads):
    """辅助函数：启动并等待所有线程"""
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# =============================================================================
# 1. Lock (threading.Lock) —— 对比 Java synchronized / ReentrantLock
# =============================================================================

def lock_demo():
    """基本互斥锁"""
    print("=" * 60)
    print("Lock（互斥锁）")
    print("=" * 60)

    # Java: lock.lock(); try { counter++; } finally { lock.unlock(); }
    lock = threading.Lock()

    def run_test(fn, n=5):
        c = {"v": 0}
        _run_threads(*[threading.Thread(target=fn, args=(c,)) for _ in range(n)])
        return c["v"]

    def unsafe(c):
        for _ in range(10000): c["v"] += 1

    def safe(c):
        for _ in range(10000):
            with lock: c["v"] += 1

    print(f"  不加锁: {run_test(unsafe)}（期望 50000，可能不一致）")
    print(f"  加锁:   {run_test(safe)}（始终 50000）")

    # tryLock —— 非阻塞获取（Java 的 lock.tryLock()）
    lk = threading.Lock()
    lk.acquire()
    print(f"  tryLock（已占用）: {lk.acquire(blocking=False)}")
    lk.release()
    print(f"  tryLock（空闲）:   {lk.acquire(blocking=False)}")
    lk.release()


# =============================================================================
# 2. RLock（可重入锁）—— 对比 Java ReentrantLock
# =============================================================================

def rlock_demo():
    """可重入锁：同一线程可多次获取"""
    print("\n" + "=" * 60)
    print("RLock（可重入锁）")
    print("=" * 60)

    # Java ReentrantLock 默认可重入；Python Lock 不可重入，RLock 才可以
    rlock = threading.RLock()

    def outer():
        with rlock:
            print("  outer 获取了锁")
            inner()

    def inner():
        with rlock:  # 同一线程再次获取 —— OK
            print("  inner 再次获取（可重入）")

    outer()

    # 普通 Lock 不可重入
    normal_lock = threading.Lock()
    normal_lock.acquire()
    print(f"  普通 Lock 再次 acquire: {normal_lock.acquire(blocking=False)}"
          "（False = 会死锁！）")
    normal_lock.release()


# =============================================================================
# 3. Condition —— 对比 Java Condition (wait/notify)
# =============================================================================

def condition_demo():
    """条件变量：生产者-消费者"""
    print("\n" + "=" * 60)
    print("Condition（条件变量）")
    print("=" * 60)

    # Java: condition.await()/signal()/signalAll()
    # Python: condition.wait()/notify()/notify_all()
    buffer, MAX_SIZE = [], 3
    cond = threading.Condition()

    def producer(name, count):
        for i in range(count):
            with cond:
                while len(buffer) >= MAX_SIZE:
                    cond.wait()
                item = f"{name}-item{i}"
                buffer.append(item)
                print(f"  [{name}] 生产: {item}  缓冲区: {len(buffer)}")
                cond.notify_all()
            time.sleep(0.02)

    def consumer(name, count):
        for _ in range(count):
            with cond:
                while not buffer:
                    cond.wait()
                item = buffer.pop(0)
                print(f"  [{name}] 消费: {item}  缓冲区: {len(buffer)}")
                cond.notify_all()
            time.sleep(0.03)

    _run_threads(threading.Thread(target=producer, args=("P1", 4)),
                 threading.Thread(target=consumer, args=("C1", 4)))
    print("  生产者-消费者完成")


# =============================================================================
# 4. Event —— 对比 Java CountDownLatch（简化版）
# =============================================================================

def event_demo():
    """事件：线程间简单信号通知"""
    print("\n" + "=" * 60)
    print("Event（事件信号）")
    print("=" * 60)

    # Java: latch.await()/countDown()  Python: event.wait()/set()
    # 区别：Event 可以 clear() 重置，CountDownLatch 不能
    start_event = threading.Event()

    def worker(name):
        print(f"  [{name}] 等待启动信号...")
        start_event.wait()
        print(f"  [{name}] 收到信号，开始工作!")

    ts = [threading.Thread(target=worker, args=(f"W-{i}",)) for i in range(3)]
    for t in ts:
        t.start()
    time.sleep(0.05)
    print("  [Main] 发送启动信号!")
    start_event.set()
    for t in ts:
        t.join()

    # 重置与超时
    start_event.clear()
    print(f"  clear() 后 is_set(): {start_event.is_set()}")
    print(f"  wait(timeout=0.05): {start_event.wait(timeout=0.05)}")


# =============================================================================
# 5. Semaphore —— 对比 Java Semaphore
# =============================================================================

def semaphore_demo():
    """信号量：控制并发访问数量"""
    print("\n" + "=" * 60)
    print("Semaphore（信号量）")
    print("=" * 60)

    # Java: new Semaphore(3); sem.acquire(); sem.release();
    pool = threading.Semaphore(3)  # 最多 3 个并发
    active, lock = {"n": 0}, threading.Lock()

    def access_db(wid):
        with pool:
            with lock: active["n"] += 1
            print(f"  [W-{wid}] 连接（活跃: {active['n']}）")
            time.sleep(0.04)
            with lock: active["n"] -= 1

    _run_threads(*[threading.Thread(target=access_db, args=(i,))
                    for i in range(6)])

    # BoundedSemaphore：release 不能超过初始值（更安全）
    bs = threading.BoundedSemaphore(2)
    bs.acquire(); bs.release()
    try: bs.release()
    except ValueError as e: print(f"  BoundedSemaphore 多释放: {e}")


# =============================================================================
# 6. Barrier —— 对比 Java CyclicBarrier
# =============================================================================

def barrier_demo():
    """屏障：多个线程在某点同步汇合"""
    print("\n" + "=" * 60)
    print("Barrier（屏障）")
    print("=" * 60)

    # Java: new CyclicBarrier(3, action); barrier.await();
    barrier = threading.Barrier(
        3, action=lambda: print("  >>> 所有线程到达屏障! <<<"))

    def worker(name, prep_time):
        print(f"  [{name}] 准备中...")
        time.sleep(prep_time)
        barrier.wait()
        print(f"  [{name}] 屏障后继续")

    _run_threads(
        threading.Thread(target=worker, args=("Fast", 0.02)),
        threading.Thread(target=worker, args=("Medium", 0.04)),
        threading.Thread(target=worker, args=("Slow", 0.06)),
    )


# =============================================================================
# 7. with 语句与锁 —— 对比 Java try-finally unlock
# =============================================================================

def with_statement_demo():
    """with 语句让锁更安全优雅"""
    print("\n" + "=" * 60)
    print("with 语句与锁")
    print("=" * 60)

    lock = threading.Lock()

    # Java: lock.lock(); try { ... } finally { lock.unlock(); }
    print("  Java 风格:")
    lock.acquire()
    try:
        print("    临界区...")
    finally:
        lock.release()

    # Python: with 自动 acquire/release，异常也安全
    print("  Python 风格（推荐）:")
    with lock:
        print("    临界区...")
    print("    锁自动释放")

    # 所有同步原语都支持 with
    print("  支持 with 的原语:")
    for name, obj in [("RLock", threading.RLock()),
                       ("Condition", threading.Condition()),
                       ("Semaphore", threading.Semaphore(1))]:
        with obj:
            print(f"    {name} -- OK")


# =============================================================================
# 8. 死锁示例和避免方法
# =============================================================================

def deadlock_demo():
    """死锁的产生与避免"""
    print("\n" + "=" * 60)
    print("死锁示例和避免方法")
    print("=" * 60)

    # 死锁原理：两个线程互相等待对方持有的锁（Java 完全相同）
    print("  死锁场景: T1(a->b) vs T2(b->a) 互相等待!")

    # --- 方法 1：固定加锁顺序 ---
    print("\n  --- 方法 1：固定加锁顺序 ---")
    la, lb = threading.Lock(), threading.Lock()
    shared = {"count": 0}

    def safe_work(_n):
        for _ in range(100):
            with la:
                with lb:
                    shared["count"] += 1

    _run_threads(*[threading.Thread(target=safe_work, args=(i,))
                    for i in range(3)])
    print(f"  结果: {shared['count']}（无死锁）")

    # --- 方法 2：使用 timeout ---
    print("\n  --- 方法 2：使用 timeout ---")
    lx, ly = threading.Lock(), threading.Lock()
    stats, sl = {"ok": 0, "fail": 0}, threading.Lock()

    def try_locks(first, second):
        for _ in range(50):
            if not first.acquire(timeout=0.01):
                with sl: stats["fail"] += 1
                continue
            got = second.acquire(timeout=0.01)
            with sl: stats["ok" if got else "fail"] += 1
            if got: second.release()
            first.release()

    _run_threads(threading.Thread(target=try_locks, args=(lx, ly)),
                 threading.Thread(target=try_locks, args=(ly, lx)))
    print(f"  成功: {stats['ok']}, 超时: {stats['fail']}")

    # --- 方法 3：高级抽象 ---
    print("\n  --- 方法 3：使用高级抽象（推荐）---")
    print("  用 queue.Queue 代替手动加锁")
    print("  Java 类比：优先用 BlockingQueue, ConcurrentHashMap")


# =============================================================================
# 运行所有 demo
# =============================================================================

if __name__ == "__main__":
    lock_demo()
    rlock_demo()
    condition_demo()
    event_demo()
    semaphore_demo()
    barrier_demo()
    with_statement_demo()
    deadlock_demo()
