import asyncio
import threading

import time
from queue import Queue

reader_writer_queue = Queue(100)

def thread_writer(write_time_delta = 1, write_time = 10): 
    start_time = time.time()
    write_counter = 0 
    while time.time() - start_time < write_time: 
        write_counter += 1
        reader_writer_queue.put(write_counter)
        time.sleep(write_time_delta)

class AsyncReader:
    def __init__(self, read_queue: Queue): 
        self.read_queue = read_queue
    
    async def write_to_something(self,): 
        counter = 0 
        while True: 
            await asyncio.sleep(0.3)
            counter += 1
            print(f'writer something {counter}')
    
    async def print_message_handler(self, message): 
        await asyncio.sleep(0.5)
        print(f"handling message {message} ")
    
    async def read_from_queue_to_async(self,): 
        while True: 
            try: 
                last_item = self.read_queue.get(timeout=0.5)
                await self.print_message_handler(last_item)
            except Exception as e:
                print("queue is empty, awaiting to free async")
                await asyncio.sleep(0.7)


async def start_all_async_main(): 
    async_reader = AsyncReader(reader_writer_queue)
    # asyncio.run(async_reader.read_from_queue_to_async())
    await asyncio.gather(async_reader.read_from_queue_to_async(), async_reader.write_to_something())

if __name__ == "__main__": 
    writer_th = threading.Thread(target=thread_writer, args=(0.1, 1,))
    writer_th.start()
    # thread_writer(0.1, 1)
    asyncio.run(start_all_async_main())
    print("got here ")
