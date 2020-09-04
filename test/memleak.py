import logging
import can
import time
import asyncio
import tracemalloc
import linecache

from context import config, target

from pathlib import Path
from configparser import ConfigParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def setup():
    cp = ConfigParser()
    cp_path = config.get('bootstrap.ini', TESTING=False)
    cp.read(cp_path.as_posix())

    return cp

def getBus(cp):
    return can.interface.Bus('can1', bustype='socketcan', bitrate='500000')

def timer():
    start_time = time.time()

    def internal_timer():
        return time.time()-start_time 

    return internal_timer

async def snapshot_loop():
    
    delta = timer()
    while True:
        await asyncio.sleep(15)
        if delta() > 15:
            snapshot = tracemalloc.take_snapshot()
            record_snapshot(snapshot, logger)
            delta = timer()

def record_snapshot(snapshot, logger, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
        ))
    top_stats = snapshot.statistics(key_type)

    logger.info("Snapshot at %s", time.ctime())
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        logger.info("#%s: %s:%s: %.1f KiB",
                index, frame.filename, frame.lineno, stat.size / 1024)
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            logger.info("   %s", line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        logger.info("%s other: %.1f KiB", len(other), size / 1024)
    total = sum(stat.size for stat in top_stats)
    logger.info("Total allocated size: %.1f KiB", total / 1024)

async def read_loop(reader, queue):
    while True:
        msg = await reader.read_canbus()
        if msg:
            reader.update_status(msg)
            await queue.put(msg)
        #logger.info(msg)

async def consumer_loop(queue):
    while True:
        msg = await queue.get()
        #logger.info(msg)

def main():
    tracemalloc.start()
    cp = setup()
    loop = asyncio.get_event_loop()

    reader = target.Target(cp['BMS_COMM'], loop)
    queue = asyncio.Queue(maxsize=10, loop=loop)
    
    loop.create_task(read_loop(reader, queue))
    loop.create_task(consumer_loop(queue))
    loop.create_task(snapshot_loop())

    try:
        loop.run_forever()
    except Exception:
        loop.close()

if __name__ == '__main__':
    main()
