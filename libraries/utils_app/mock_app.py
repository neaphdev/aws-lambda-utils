import random
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


def simulate_response(
    response_correct: any,
    response_failed: any,
    percentage_success: any,
    mock_responses: bool,
):
    """This decorator is used to mock the return value of a function.
    percentage_success is the percentage of success of the mocked response (0,100).
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if mock_responses:
                if random.randint(0, 100) < percentage_success:
                    print(
                        f"{__name__}:Mocking return value of {func.__name__} to {response_correct}"
                    )
                    return response_correct
                else:
                    print(
                        f"{__name__}:Mocking return value of {func.__name__} to {response_failed}"
                    )
                    return response_failed

            return func(*args, **kwargs)

        return wrapper

    return decorator


@simulate_response(
    response_correct=42,
    response_failed=0,
    percentage_success=90,
    mock_responses=True,
)
def my_function():
    print("Hello from my_function")
    return 42


if __name__ == "__main__":
    for k in range(10):
        print(my_function())
