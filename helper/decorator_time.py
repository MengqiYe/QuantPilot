import time

# 带时间统计的装饰器
def query_timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter_ns() - start) / 1e6
        print(f"Query executed in {elapsed:.2f}ms")
        return result
    return wrapper
