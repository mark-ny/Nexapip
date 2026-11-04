"""Chronological walk-forward split helper."""

def walk_forward_indices(length: int, train_size: int, test_size: int, step: int | None = None):
    if min(length, train_size, test_size) < 1:
        raise ValueError("length, train_size, and test_size must be positive")
    step = test_size if step is None else step
    if step < 1:
        raise ValueError("step must be positive")
    start = 0
    while start + train_size + test_size <= length:
        yield (range(start, start + train_size),
               range(start + train_size, start + train_size + test_size))
        start += step
