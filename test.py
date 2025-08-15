import numpy as np

arr = np.array([1, 2, 3, 4, 5])

def my_filter(x):
    return x % 2 == 0  # Оставляем только чётные числа

vectorized_filter = np.vectorize(my_filter)
print(vectorized_filter)
mask = vectorized_filter(arr)  # [False, True, False, True, False]
print(mask)
filtered_arr = arr[mask]  # [2, 4]
print(filtered_arr)