import numpy as np

from . import model_evaluation
from .factor_tools import factor_match_score


# TODO: Tests for similarity_evaluation
# Set similarity metric to a function that only return ones to check that the argument is used
# Check comparison tensors equal to cp_tensor to check that we only get ones
# Test with CP tensors with known similarity
def similarity_evaluation(
    cp_tensor, comparison_cp_tensors, similarity_metric=None, **kwargs
):
    """Compute similarities between ``cp_tensor`` and all ``comparison_cp_tensors``.

    Parameters
    ----------
    cp_tensor : CPTensor or tuple
        TensorLy-style CPTensor object or tuple with weights as first
        argument and a tuple of components as second argument
    comparison_cp_tensors : List[CPTensor or tuple]
        List of TensorLy-style CPTensors to compare with
    similarity_metric : Callable[CPTensor, CPTensor, **kwargs] -> float
        Function that takes two CPTensors as input and returns their similarity
    **kwargs
        Extra keyword-arguments passed to ``similarity_metric``.

    Returns
    -------
    similarity : float
    """
    # TODO: example for similarity_evaluation
    if similarity_metric is None:
        similarity_metric = factor_match_score

    return [
        similarity_metric(cp_tensor, comparison_cp_tensor, **kwargs)
        for comparison_cp_tensor in comparison_cp_tensors
    ]


def get_model_with_lowest_error(cp_tensors, X, error_function=None):
    """Compute reconstruction error for all cp_tensors and return model with lowest error.

    This is useful to select the best initialisation if several random
    initialisations are used to fit the model. By default, the relative SSE
    is used, but another error function can be used too.

    Parameters
    ----------
    cp_tensors : list of CPTensors
        List of all CP tensors to compare
    X : ndarray
        Dataset modelled by the CP tensors
    error_function : Callable (optional)
        Callable with the signature ``error_function(cp_tensor, X)``,
        that should return a measure of the modelling error (e.g. SSE).

    Returns
    -------
    CPTensor
        The CP tensor with the lowest error
    int
        The index of the selected CP tensor in ``cp_tensors``
    list
        List of the error values for all CP tensors in ``cp_tensor``
        (in the same order as ``cp_tensors``).
    """
    # TODO: tests for get_model_with_lowest_error
    # TODO: example for get_model_with_lowest_error
    if error_function is None:
        error_function = model_evaluation.relative_sse

    selected_cp_tensor = None
    selected_index = None
    lowest_sse = np.inf
    all_sse = []
    for i, cp_tensor in enumerate(cp_tensors):
        sse = error_function(cp_tensor, X)
        all_sse.append(sse)
        if sse < lowest_sse:
            selected_cp_tensor = cp_tensor
            lowest_sse = sse
            selected_index = i

    return selected_cp_tensor, selected_index, all_sse


def sort_models_by_error(cp_tensors, X, error_function=None):
    """Sort the ``cp_tensors`` by their error so the model with the lowest error is first.

    Parameters
    ----------
    cp_tensors : list of CPTensors
        List of all CP tensors
    X : ndarray
        Dataset modelled by the CP tensors
    error_function : Callable (optional)
        Callable with the signature ``error_function(cp_tensor, X)``,
        that should return a measure of the modelling error (e.g. SSE).

    Returns
    -------
    list of CPTensors
        List of all CP tensors sorted so the CP tensor with the lowest error
        is first and highest error is last.
    """
    # TODO: examples for sort_models_by_error
    # TODO: tests for sort_models_by_error: Create one CP tensor, create copies where A is multiplied by 2, 3, 4, 5, etc. Shuffle copies, check that after sorting, they are in right order.
    errors = get_model_with_lowest_error(cp_tensors, X, error_function=error_function)[
        2
    ]
    sorted_tensors = sorted(zip(errors, cp_tensors))
    # We use np.asarray(error).item() because the error is an XArray object for X-array datasets
    return (
        [cp_tensor for error, cp_tensor in sorted_tensors],
        [np.asarray(error).item() for error, cp_tensor in sorted_tensors],
    )
