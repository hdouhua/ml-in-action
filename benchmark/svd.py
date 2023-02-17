import time
import numpy as np
np.random.seed(42)
a = np.random.uniform(size=(300, 300))
RUNTIMES = 10

timecosts = []
for _ in range(RUNTIMES):
    s_time = time.time()
    for i in range(100):
        a += 1
        np.linalg.svd(a)
    timecosts.append(time.time() - s_time)

print(f'mean of {RUNTIMES} runs: {np.mean(timecosts):.5f}s')
