import time


def timer(func):
    """
    Decorator to measure the execution time of a function. This is useful for benchmarking and to measure the execution time of a function that takes no arguments.

    Args:
        func: The function to be timed. Should be a function of the form func ( * args ** kwargs )

    Returns:
        The result of the time taken for the running of the function
    """

    def wrapper(*args, **kwargs):
        """
        Wrapper to print execution time. This is used as a decorator for multiprocessing. Process. The arguments to pass to the function.


        Returns:
                The return value of the function that was called with the arguments passed to it. It is returned as - is
        """
        print(f"Timed process starting function: {func.__qualname__} ....")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.5f} seconds")
        return result

    return wrapper
