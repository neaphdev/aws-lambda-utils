from typing import Any


def mock_return(
    value: Any,
    mock_responses: bool,
):
    """This decorator is used to mock the return value of a function."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            if mock_responses:
                print(f"{__name__}:Mocking return value of {func.__name__} to {value}")
                return value
            return func(*args, **kwargs)

        return wrapper

    return decorator
