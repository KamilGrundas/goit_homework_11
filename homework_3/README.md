# Homework #3

## Part 1: Threads

Create a program to work with the "Mess" folder, which will sort the files in the given folder by extensions using multiple threads. Speed up the processing of large directories with many subfolders and files by processing each folder in parallel threads. The most time-consuming task will be moving the files and creating a list of files in the folder (iterating through the entire directory contents). To speed up the transfer of files, this can be done in a separate thread or a thread pool. This will be more convenient since the result of this operation will not be processed in the application, and no results need to be collected. To speed up traversing through a directory with a large number of subdirectories, each of these subdirectories can be processed in a separate thread or passed to a thread pool for processing.

## Part 2: Processes

Implement the `factorize` function, which takes a list of numbers and returns a list of numbers that divide the input numbers without a remainder.

Implement a synchronous version and measure the execution time.

Next, improve the performance of your function by utilizing multiple CPU cores for parallel computations, and again measure the execution time. To determine the number of cores on your machine, use the `cpu_count()` function from the `multiprocessing` package.

The correctness of the algorithm can be verified with the following test:

```python
def factorize(*numbers):
    # YOUR CODE HERE
    raise NotImplementedError()  # Remove after implementation

a, b, c, d = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
```