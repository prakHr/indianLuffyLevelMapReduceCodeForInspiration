import numpy as np
from pargraph import graph, delayed


@delayed
def filter_array(
    array: np.ndarray,
    low: float,
    high: float,
    include_low: bool = True,
    include_high: bool = False,
) -> np.ndarray:

    if include_low and include_high:
        mask = (array >= low) & (array <= high)
    elif include_low:
        mask = (array >= low) & (array < high)
    else:
        mask = (array > low) & (array <= high)

    return array[mask]


@delayed
def sort_array(array: np.ndarray) -> np.ndarray:
    return np.sort(array)


@delayed
def reduce_arrays(*arrays: np.ndarray) -> np.ndarray:
    if not arrays:
        return np.array([], dtype=float)

    return np.concatenate(arrays)


@graph
def map_reduce_sort(
    array: np.ndarray,
    partition_count: int,
) -> np.ndarray:

    if len(array) == 0:
        return np.array([])

    minimum = np.min(array)
    maximum = np.max(array)

    if minimum == maximum:
        return array

    boundaries = np.linspace(
        minimum,
        maximum,
        partition_count + 1,
    )

    partitions = []

    for i in range(partition_count):
        low = boundaries[i]
        high = boundaries[i + 1]

        # Last partition includes its upper boundary.
        if i == partition_count - 1:
            filtered = filter_array(
                array,
                low,
                high,
                True,
                True,
            )
        else:
            filtered = filter_array(
                array,
                low,
                high,
                True,
                False,
            )

        partitions.append(
            sort_array(filtered)
        )

    return reduce_arrays(*partitions)


def scalable_sort(arr, partition_count=4):

    arr = np.asarray(arr)

    negative = arr[arr < 0]
    positive = arr[arr >= 0]

    # Sort absolute values of negative numbers.
    if len(negative):
        negative_abs = np.abs(negative)

        sorted_negative_abs = map_reduce_sort(
            negative_abs,
            partition_count,
        )

        # Restore negative sign and reverse.
        sorted_negative = (
            sorted_negative_abs * -1
        )[::-1]

    else:
        sorted_negative = np.array([], dtype=arr.dtype)

    # Sort non-negative numbers.
    if len(positive):
        sorted_positive = map_reduce_sort(
            positive,
            partition_count,
        )

    else:
        sorted_positive = np.array([], dtype=arr.dtype)

    return np.concatenate(
        [
            sorted_negative,
            sorted_positive,
        ]
    )


def get_top_k_elements(
    np_array_sorted,
    top_k,
):
    return np_array_sorted[::-1][:top_k]


def get_bottom_k_elements(
    np_array_sorted,
    bottom_k,
):
    return np_array_sorted[:bottom_k]


def optimized_scalable_sort(
    np_array,
    partition_count,
):
    np_array_sorted = scalable_sort(
        np_array,
        partition_count,
    )

    return {
        "np_array_sorted": np_array_sorted,
        "np_array_size": len(np_array),
    }


def optimized_scalable_topk_elements_getter(
    np_array,
    partition_count,
    top_k,
):
    np_array_sorted = scalable_sort(
        np_array,
        partition_count,
    )

    top_k_elements = get_top_k_elements(
        np_array_sorted,
        top_k,
    )

    return {
        "top_k_elements": top_k_elements,
        "top_k": len(top_k_elements),
    }


def optimized_scalable_bottomk_elements_getter(
    np_array,
    partition_count,
    bottom_k,
):
    np_array_sorted = scalable_sort(
        np_array,
        partition_count,
    )

    bottom_k_elements = get_bottom_k_elements(
        np_array_sorted,
        bottom_k,
    )

    return {
        "bottom_k_elements": bottom_k_elements,
        "bottom_k": len(bottom_k_elements),
    }


if __name__ == "__main__":

    partition_count = 4
    N = pow(10,8)
    include_only_unique = False
    arr = [i for i in range(N)] + [0] + [-1*i for i in range(N)]
    if include_only_unique==True:
        st = set()
        arr2 = []
        for ele in arr:
            if ele not in st:
                arr2.append(ele)
                st.add(ele)
        arr = arr2
    np_array = np.array(arr)

    print(
        optimized_scalable_sort(
            np_array,
            partition_count,
        )
    )

    top_k = 10

    print(
        optimized_scalable_topk_elements_getter(
            np_array,
            partition_count,
            top_k,
        )
    )

    bottom_k = 10

    print(
        optimized_scalable_bottomk_elements_getter(
            np_array,
            partition_count,
            bottom_k,
        )
    )
