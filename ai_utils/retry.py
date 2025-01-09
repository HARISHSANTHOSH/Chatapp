import random
import time

import openai


# NOTE change backoff to use tenacity if required.
def retry_with_exponential_backoff(func):
    """Retries a function with exponential backoff on specific errors.

    This decorator retries the wrapped function upon encountering specific errors
    related to the OpenAI API. It uses an exponential backoff strategy with optional
    jitter to avoid overwhelming the API. The function will be retried up to a maximum
    number of attempts before giving up and returning an error message.

    Args:
        func (Callable): The function to be wrapped and retried.

    Returns:
        Callable: A wrapper function that handles retrying the original function.

    Raises:
        Exception: Re-raises any exceptions that are not part of the specified errors to retry.

    Returns:
        Tuple[bool, Any]:
            - A boolean indicating success (True) or failure (False) of the function call.
            - The result of the function call if successful, or an error message if retries are exhausted.

    Attributes:
        initial_delay (float): Initial delay before the first retry attempt, in seconds.
        exponential_base (int): The base of the exponential backoff multiplier.
        jitter (bool): Whether to apply a random jitter to the backoff delay.
        max_retries (int): Maximum number of retries before giving up.
        errors (Tuple[Type[Exception], ...]): A tuple of exceptions that trigger a retry.
    """

    def wrapper(*args, **kwargs):
        initial_delay = 1
        exponential_base = 2
        jitter = True
        max_retries = 3
        errors = (
            openai.RateLimitError,
            openai.APITimeoutError,
            openai.APIConnectionError,
            openai.APIStatusError,
        )

        num_retries = 0
        delay = initial_delay

        while True:
            try:
                return True, func(*args, **kwargs)
            except errors as e:
                num_retries += 1
                if num_retries > max_retries:
                    error_str = f"Maximum number of retries ({max_retries}) exceeded with exception: {e}."
                    return False, error_str

                delay *= exponential_base * (1 + jitter * random.random())
                time.sleep(delay)
            except Exception as e:
                raise e

    return wrapper
