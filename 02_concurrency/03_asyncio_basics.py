"""
Python3 asyncio 异步编程 —— 写给 Java 开发者

核心概念：
- asyncio 是 Python 的协程框架，单线程实现高并发
- 类比 Java: 类似 CompletableFuture + 事件循环，但语法更优雅
- async/await 语法让异步代码看起来像同步代码
"""

import asyncio
import time
import random


# =============================================================================
# 1. async/await 基础
# =============================================================================

async def async_await_basics():
    """async/await 基本用法 —— 对比 Java CompletableFuture / Kotlin coroutines"""
    print("=" * 60)
    print("async/await 基础")
    print("=" * 60)

    # Java:  CompletableFuture.supplyAsync(() -> { ... }).get();
    # Kotlin: suspend fun fetchData(): String { delay(1000); return "结果" }
    # Python: async def 定义协程，await 等待结果

    async def fetch_data(name, delay_sec):
        """模拟异步 IO 操作"""
        print(f"  [{name}] 开始请求...")
        await asyncio.sleep(delay_sec)  # 非阻塞等待，类似 Kotlin delay()
        print(f"  [{name}] 请求完成")
        return f"{name} 的数据"

    result = await fetch_data("API-1", 0.3)
    print(f"  结果: {result}")

    # 调用 async 函数不会立即执行，只是创建协程对象
    coro = fetch_data("API-2", 0.1)
    print(f"  协程对象: {coro}")
    result = await coro  # 必须 await 才会执行
    print(f"  结果: {result}")


# =============================================================================
# 2. 协程的创建和运行 (asyncio.run)
# =============================================================================

async def coroutine_run_demo():
    """协程的创建和运行方式"""
    print("\n" + "=" * 60)
    print("协程的创建和运行")
    print("=" * 60)

    # asyncio.run() 是顶层入口，创建事件循环并运行协程
    # 类比 Java: ExecutorService 的 submit + get

    async def step_one():
        print("  步骤一: 获取用户信息...")
        await asyncio.sleep(0.2)
        return {"id": 1, "name": "张三"}

    async def step_two(user):
        print(f"  步骤二: 查询 {user['name']} 的订单...")
        await asyncio.sleep(0.2)
        return [{"order_id": 101, "amount": 99.9}]

    # 串行执行——每一步依赖上一步的结果
    start = time.perf_counter()
    user = await step_one()
    orders = await step_two(user)
    total = sum(o["amount"] for o in orders)
    elapsed = time.perf_counter() - start
    print(f"  用户: {user['name']}, 订单总额: {total}, 耗时: {elapsed:.2f}s")


# =============================================================================
# 3. asyncio.gather 并发执行
# =============================================================================

async def gather_demo():
    """asyncio.gather —— 对比 Java CompletableFuture.allOf"""
    print("\n" + "=" * 60)
    print("asyncio.gather 并发执行")
    print("=" * 60)

    # Java: CompletableFuture.allOf(f1, f2, f3).join();
    # Python: asyncio.gather 并发执行多个协程，收集所有结果

    async def call_api(name, delay_sec):
        print(f"  [{name}] 发起请求...")
        await asyncio.sleep(delay_sec)
        return f"{name}: OK"

    # 串行 vs 并发对比
    start = time.perf_counter()
    r1 = await call_api("用户服务", 0.3)
    r2 = await call_api("订单服务", 0.3)
    serial_time = time.perf_counter() - start
    print(f"  串行耗时: {serial_time:.2f}s")

    start = time.perf_counter()
    results = await asyncio.gather(
        call_api("用户服务", 0.3),
        call_api("订单服务", 0.3),
    )
    gather_time = time.perf_counter() - start
    print(f"  并发耗时: {gather_time:.2f}s (快了约 {serial_time / gather_time:.1f} 倍)")

    # return_exceptions=True: 不会因单个失败而中断
    async def may_fail(name):
        if name == "坏服务":
            raise ValueError(f"{name} 挂了")
        await asyncio.sleep(0.1)
        return f"{name}: OK"

    print("\n  --- return_exceptions=True ---")
    results = await asyncio.gather(
        may_fail("好服务"), may_fail("坏服务"), return_exceptions=True,
    )
    for r in results:
        print(f"  {'异常' if isinstance(r, Exception) else '成功'}: {r}")


# =============================================================================
# 4. asyncio.create_task
# =============================================================================

async def create_task_demo():
    """asyncio.create_task —— 后台调度协程"""
    print("\n" + "=" * 60)
    print("asyncio.create_task")
    print("=" * 60)

    # 类比 Java: executor.submit(callable) 返回 Future
    # Task 可以 await、取消、查询状态

    async def background_job(name, delay_sec):
        print(f"  [{name}] 后台任务启动")
        await asyncio.sleep(delay_sec)
        print(f"  [{name}] 后台任务完成")
        return f"{name} 结果"

    task1 = asyncio.create_task(background_job("任务A", 0.3))
    task2 = asyncio.create_task(background_job("任务B", 0.2))
    print(f"  创建后立即查询: task1.done={task1.done()}, task2.done={task2.done()}")

    print("  主协程: 做其他工作...")
    await asyncio.sleep(0.1)

    result1 = await task1
    result2 = await task2
    print(f"  task1={result1}, task2={result2}")

    # 取消 Task
    print("\n  --- Task 取消 ---")

    async def long_running():
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            print("  [长任务] 被取消了，执行清理...")
            raise

    task3 = asyncio.create_task(long_running())
    await asyncio.sleep(0.1)
    task3.cancel()
    try:
        await task3
    except asyncio.CancelledError:
        print(f"  task3 已取消, cancelled={task3.cancelled()}")


# =============================================================================
# 5. 异步迭代器和异步生成器
# =============================================================================

async def async_iterator_demo():
    """async for 和 async yield"""
    print("\n" + "=" * 60)
    print("异步迭代器和异步生成器")
    print("=" * 60)

    # 类比 Java: 没有直接对应，类似 Reactor Flux

    async def fetch_pages(total_pages):
        """模拟分页请求 —— 异步生成器"""
        for page in range(1, total_pages + 1):
            await asyncio.sleep(0.1)
            data = [f"page{page}_item{i}" for i in range(3)]
            yield page, data  # async yield

    print("  --- 异步生成器 ---")
    async for page_num, items in fetch_pages(3):
        print(f"  第{page_num}页: {items}")

    # 异步迭代器类：实现 __aiter__ 和 __anext__
    class AsyncCountdown:
        def __init__(self, start):
            self.current = start

        def __aiter__(self):
            return self

        async def __anext__(self):
            if self.current <= 0:
                raise StopAsyncIteration
            await asyncio.sleep(0.05)
            self.current -= 1
            return self.current + 1

    print("\n  --- 异步迭代器类 ---")
    async for num in AsyncCountdown(5):
        print(f"  倒计时: {num}")

    # 异步列表推导
    results = [item async for _, items in fetch_pages(2) for item in items]
    print(f"\n  异步列表推导: {results}")


# =============================================================================
# 6. asyncio.Queue —— 异步队列
# =============================================================================

async def async_queue_demo():
    """asyncio.Queue —— 生产者消费者模式"""
    print("\n" + "=" * 60)
    print("asyncio.Queue 异步队列")
    print("=" * 60)

    # 类比 Java: BlockingQueue，但完全非阻塞

    queue = asyncio.Queue(maxsize=5)

    async def producer(name, count):
        for i in range(count):
            item = f"{name}-消息{i}"
            await queue.put(item)
            print(f"  [生产者 {name}] 放入: {item}")
            await asyncio.sleep(random.uniform(0.05, 0.1))

    async def consumer(name):
        consumed = 0
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=0.4)
                print(f"  [消费者 {name}] 取出: {item}")
                queue.task_done()
                consumed += 1
            except asyncio.TimeoutError:
                print(f"  [消费者 {name}] 超时退出，共消费 {consumed} 条")
                break

    await asyncio.gather(
        producer("P1", 3), producer("P2", 3), consumer("C1"), consumer("C2"),
    )
    print(f"  队列剩余: {queue.qsize()}")


# =============================================================================
# 7. asyncio.wait_for 超时控制
# =============================================================================

async def timeout_demo():
    """asyncio.wait_for —— 超时控制"""
    print("\n" + "=" * 60)
    print("asyncio.wait_for 超时控制")
    print("=" * 60)

    # 类比 Java: future.get(timeout, TimeUnit.SECONDS)

    async def slow_operation():
        await asyncio.sleep(5)
        return "慢操作结果"

    print("  --- 慢操作（超时 0.3s）---")
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=0.3)
        print(f"  结果: {result}")
    except asyncio.TimeoutError:
        print("  超时了！操作被取消")

    # 带超时的重试模式
    print("\n  --- 带超时的重试模式 ---")

    async def unreliable_service():
        delay = random.uniform(0.1, 0.6)
        await asyncio.sleep(delay)
        return f"响应(耗时{delay:.2f}s)"

    for attempt in range(1, 4):
        try:
            result = await asyncio.wait_for(unreliable_service(), timeout=0.3)
            print(f"  第{attempt}次: 成功 - {result}")
            break
        except asyncio.TimeoutError:
            print(f"  第{attempt}次: 超时，重试...")
    else:
        print("  所有重试都失败了")


# =============================================================================
# 8. 事件循环概念
# =============================================================================

async def event_loop_demo():
    """事件循环 (Event Loop) 概念"""
    print("\n" + "=" * 60)
    print("事件循环概念")
    print("=" * 60)

    # 类比 Java: Netty EventLoop / NIO Selector
    # 类比 JS: Node.js 事件循环
    # 工作原理: 单线程轮询，遇到 await 挂起，IO 完成后恢复

    loop = asyncio.get_running_loop()
    print(f"  当前事件循环: {type(loop).__name__}")
    print(f"  是否在运行: {loop.is_running()}")

    # 演示交替调度
    async def task_with_id(task_id, steps):
        for step in range(steps):
            print(f"  [Task-{task_id}] 第 {step + 1} 步")
            await asyncio.sleep(0)  # yield 控制权

    print("\n  --- 事件循环调度（交替执行）---")
    await asyncio.gather(task_with_id("A", 3), task_with_id("B", 3))

    # call_soon / call_later
    print("\n  --- call_later 延时回调 ---")
    result_holder = []
    loop.call_soon(lambda: result_holder.append("立即"))
    loop.call_later(0.1, lambda: result_holder.append("0.1s后"))
    await asyncio.sleep(0.2)
    print(f"  回调结果: {result_holder}")


# =============================================================================
# 9. 适用场景：高并发 IO
# =============================================================================

async def real_world_scenario():
    """实战场景：高并发 IO（Web 服务、爬虫、微服务调用）"""
    print("\n" + "=" * 60)
    print("实战场景：高并发 IO")
    print("=" * 60)

    # 适合: Web 服务(FastAPI)、爬虫、微服务调用、WebSocket、异步 DB
    # 不适合: CPU 密集型（用 multiprocessing）

    async def call_microservice(name, latency):
        await asyncio.sleep(latency)
        return {"service": name, "status": "ok", "ms": int(latency * 1000)}

    # 微服务聚合（API Gateway 模式）
    print("  --- 微服务聚合 ---")
    start = time.perf_counter()
    results = await asyncio.gather(
        call_microservice("用户中心", 0.2),
        call_microservice("订单系统", 0.3),
        call_microservice("支付网关", 0.15),
        call_microservice("库存服务", 0.25),
    )
    elapsed = time.perf_counter() - start
    for r in results:
        print(f"  {r['service']}: {r['status']} ({r['ms']}ms)")
    print(f"  总耗时: {elapsed:.2f}s (最慢服务 0.3s，并发所以总时间约等于最慢的)")

    # 限流爬虫（Semaphore 控制并发度）
    print("\n  --- 限流爬虫（Semaphore）---")
    semaphore = asyncio.Semaphore(3)

    async def crawl_url(url):
        async with semaphore:  # 最多 3 个并发
            print(f"  爬取: {url}")
            await asyncio.sleep(random.uniform(0.1, 0.2))
            return f"{url} -> 200"

    urls = [f"https://example.com/page/{i}" for i in range(6)]
    start = time.perf_counter()
    results = await asyncio.gather(*[crawl_url(u) for u in urls])
    elapsed = time.perf_counter() - start
    print(f"  完成 {len(results)} 个请求, 耗时: {elapsed:.2f}s (并发度=3)")


# =============================================================================
# 运行所有 demo
# =============================================================================

async def main():
    """主入口：按顺序运行所有演示"""
    await async_await_basics()
    await coroutine_run_demo()
    await gather_demo()
    await create_task_demo()
    await async_iterator_demo()
    await async_queue_demo()
    await timeout_demo()
    await event_loop_demo()
    await real_world_scenario()


if __name__ == "__main__":
    # asyncio.run() 是 Python 3.7+ 的推荐入口
    # 创建事件循环 -> 运行协程 -> 关闭循环
    # 类比 Java: SpringApplication.run() 启动异步运行时
    asyncio.run(main())
