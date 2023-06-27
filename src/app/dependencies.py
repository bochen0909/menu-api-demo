from typing import Annotated



def get_memory_dao():
    from .dao import memory
    return memory

def get_elasticsearch_dao():
    from .dao import elasticsearch
    return elasticsearch

async def get_dao():
    return get_elasticsearch_dao()