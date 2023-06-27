from typing import Annotated



def get_memory_dao():
    from .dao import memory
    return memory


async def get_dao():
    return get_memory_dao()