import os

def get_memory_dao():
    from .dao import memory
    return memory

def get_elasticsearch_dao():
    from .dao import elasticsearch
    return elasticsearch

async def get_dao():
    if os.environ.get("MEMORY_ONLY", 'false').lower() in ['1','true','yes']:
        return get_memory_dao()
    else:
        return get_elasticsearch_dao()