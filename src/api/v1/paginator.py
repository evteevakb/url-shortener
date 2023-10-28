"""Contains paginator"""
from typing import Dict

from fastapi import Query


def get_pagination_parameters(
    max_result: int = Query(default=10, ge=1, alias='max-result'),
    offset: int = Query(default=0, ge=0, alias='offset')) -> Dict[str, int]:
    """Returns pagination parameters.

    Args:
        max_result (int, optional): number of rows returned by a query. Defaults to 10.
        offset (int, optional): skips the query by the specified number of rows. Defaults to 0.

    Returns:
        Dict[str, int]: pagination parameters.
    """
    return {"max_result": max_result, "offset": offset}
