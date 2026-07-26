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


def optimized_scalable_sort(np_array, partition_count):
    np_array = np_array/len(np_array)
    np_array_sorted = map_reduce_sort(np_array, partition_count)*len(np_array)
    return {"np_array_sorted":np_array_sorted,"np_array_size":len(np_array)}

def optimized_scalable_topk_elements_getter(np_array, partition_count, top_k):
    np_array = np_array/len(np_array)
    np_array_sorted = (map_reduce_sort(np_array, partition_count)*len(np_array))[:top_k]
    return {"top_k_elements":np_array_sorted,"top_k":len(np_array_sorted)}

def optimized_scalable_bottomk_elements_getter(np_array, partition_count, bottom_k):
    np_array = np_array/len(np_array)
    np_array_sorted = ((map_reduce_sort(np_array, partition_count)*len(np_array))[::-1])[:bottom_k]
    return {"bottom_k_elements":np_array_sorted,"bottom_k":len(np_array_sorted)}

    

    

if __name__=="__main__":
    N = int(pow(10,8))
    partition_count = 4
    arr = [i for i in range(N)]
    np_array = np.array(arr)
    array_data_dict = optimized_scalable_sort(np_array, partition_count)
    from pprint import pprint
    pprint(array_data_dict)

    top_k = 100
    array_data_dict = optimized_scalable_topk_elements_getter(np_array, partition_count, top_k)
    pprint(array_data_dict)

    bottom_k = 100
    array_data_dict = optimized_scalable_bottomk_elements_getter(np_array, partition_count, bottom_k)
    pprint(array_data_dict)
