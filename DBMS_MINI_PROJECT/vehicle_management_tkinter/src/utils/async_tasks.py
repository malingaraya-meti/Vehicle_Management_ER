import asyncio
from concurrent.futures import ThreadPoolExecutor

def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        return loop.run_in_executor(executor, func, *args)

async def load_data_async(load_function, *args):
    return await run_in_executor(load_function, *args)

async def save_data_async(save_function, *args):
    return await run_in_executor(save_function, *args)