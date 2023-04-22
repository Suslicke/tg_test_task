from functools import wraps
from inspect import iscoroutinefunction

#Used when registering commands
commands_dict = {}
#Decorator for creationg data in commands_dict
def register_command(commands_list):
    def decorator(func):
        if not iscoroutinefunction(func):
            raise TypeError('unsupported callable, expected an async function')

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        commands_dict[func.__name__] = commands_list
        return wrapper

    return decorator