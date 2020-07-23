from types import FunctionType, ModuleType
from typing import *


def create_func(func: FunctionType) -> FunctionType:
    """Creates the actual function"""
    
    def actual_func(*args, **kwargs):
        return func(*args, **kwargs)
    
    return actual_func


def create_name(module: ModuleType, func_name: str) -> str:
    """Creates the name for the tag"""
    
    return f"{module.__name__}.{func_name}"


def iter_module(module: ModuleType) -> Generator[Tuple[str, FunctionType], ModuleType, None]:
    """Iterates over the module's functions"""
    
    for name in dir(module):
        
        if not (name.startswith("_") or name.endswith("_")) and \
                hasattr((func := getattr(module, name)), "__call__"):
            yield create_name(module, name), create_func(func)
