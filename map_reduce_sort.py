import numpy as np
from pargraph import graph, delayed


@delayed
def filter_array(array: np.ndarray, low: float, high: float) -> np.ndarray:
    return array[(array >= low) & (array <= high)]


@delayed
def sort_array(array: np.ndarray) -> np.ndarray:
    return np.sort(array)


@delayed
def reduce_arrays(*arrays: np.ndarray) -> np.ndarray:
    return np.concatenate(arrays)


@graph
def map_reduce_sort(array: np.ndarray, partition_count: int) -> np.ndarray:
    return reduce_arrays(
        *(
            sort_array(filter_array(array, i / partition_count, (i +
1) / partition_count))
            for i in range(partition_count)
        )
    )


def optimized_scalable_sort(N,partition_count):
    np_array = map_reduce_sort(np.random.rand(N),partition_count)
    return {"np_array":np_array,"np_array_size":len(np_array)}

# if __name__=="__main__":
#     N = int(pow(10,8))
#     partition_count = 4
#     array_data_dict = optimized_scalable_sort(N,partition_count)
#     from pprint import pprint
#     pprint(array_data_dict)
