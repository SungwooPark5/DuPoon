def create_slippage_fn(rate: float):
    """
    Create a slippage function that returns a fixed slippage value.
    :param rate: The slippage rate as a percentage (e.g., 0.01 for 1%).
    :return: A function that calculates slippage based on quantity and price.
    """

    def slippage_fn(q, p):
        return max(1, rate * abs(q))

    return slippage_fn
