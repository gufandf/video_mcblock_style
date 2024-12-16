import threading
import time

# 设置最大允许同时运行的线程数量
MAX_THREADS = 3
semaphore = threading.Semaphore(MAX_THREADS)

def worker(semaphore):
    with semaphore:
        # 线程的工作内容
        print(f'{threading.current_thread().getName()} is working')
        # 模拟一些耗时操作
        time.sleep(1)
        print(f'{threading.current_thread().getName()} has finished')

# 创建多个线程
threads = []
for i in range(10):
    thread = threading.Thread(target=worker, args=(semaphore,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

print('All threads have finished their work.')
