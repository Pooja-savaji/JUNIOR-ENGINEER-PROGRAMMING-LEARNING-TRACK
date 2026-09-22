import pandas as pd
import time
df = pd.DataFrame({"price": range(1, 1000001)})

start = time.time()           # Slow method
result1 = []
for price in df["price"]:
    result1.append(price * 2)
slow_time = time.time() - start

start = time.time()        #  Vectorized method
result2 = df["price"] * 2
fast_time = time.time() - start
print("Slow time:", slow_time)
print("Vectorized time:", fast_time)
