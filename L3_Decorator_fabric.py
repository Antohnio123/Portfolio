from functools import wraps


def apply(func2: callable) -> any:
    """It decors a function and gives its stdout to the second function, that it has as the first attribute.
    Returns a result (stdout) of an attribute function.
    :func2: attribute function, that needs to get the result of other one (func1).
    :func1: a decorated function, that takes attributes from stdin and gives its result to the next function in pipeline - func2.
    """
    def decor(func1: callable):
        @wraps(func1)
        def wrapper1(*args, ** kwargs):
            inner_result = func1(*args, ** kwargs)
            upper_result = func2(inner_result)
            return upper_result
        return wrapper1
    return decor


def test_function(a: int) -> int:
    """Any function. Let's multiply by 1000, for example."""
    return a * 1000


@apply(test_function)
def return_user_id(k: int = 42) -> int:
    """Any function. Let's return our attribute. Default is integer number 42."""
    return k


print(return_user_id(3))

