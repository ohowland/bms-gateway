""" Gateway reads, translates, and writes CANbus frames.

    Author: Owen Edgerton
    For: Howl & Edgerton, LLC
    Date: 8/15/20
"""

import asyncio
import logging
import time
import tracemalloc
import linecache
import sys

LOGGER = logging.getLogger()

def timer():
    start_time = time.time()

    def internal_timer():
        return time.time()-start_time 

    return internal_timer

async def snapshot_loop():

    stats_logger = logging.getLogger()
    stats_handler = logging.FileHandler('hourly_top_stats.txt')
    stats_handler.setLevel(logging.INFO)
    stats_logger.addHandler(stats_handler)
    
    delta = timer()
    while True:
        await asyncio.sleep(30)
        if delta() > 30:
            snapshot = tracemalloc.take_snapshot()
            record_snapshot(snapshot, stats_logger)
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
