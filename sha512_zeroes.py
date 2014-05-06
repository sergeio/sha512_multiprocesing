from __future__ import print_function

from hashlib import sha512
from multiprocessing import Process, Queue, active_children
from time import sleep
import sys


def main():
    if len(sys.argv) < 3:
        print('Usage: python sha_512_zeroes.py num_zeroes num_processes')
        sys.exit(1)
    zeroes = int(sys.argv[1])
    procs = int(sys.argv[2])
    print(get_hash_with_leading_zeroes(num_zeroes=zeroes, num_processes=procs))


def get_hash_with_leading_zeroes(num_zeroes, num_processes):
    """Look for an integer, whose hash starts with `num_zeroes` leading zeroes.

    Spawn a maximum `num_processes` processes to do this in parallel.

    """
    result_queue = Queue()
    process_spawner = spawn_processes(num_processes, num_zeroes, result_queue)

    # Blocks until some process finds the hash we are looking for.
    result = result_queue.get()
    process_spawner.terminate()
    return result


def spawn_processes(max_processes, num_zeroes, result_queue):
    """Start a process that will spawn processes to look for our hash.

    The process-spawning process is not a daemon as daemons can't spawn
    subprocesses.

    The process is returned by the function, **to be terminated manually**.

    """
    def _process_spawner():
        """Keep spawning processes to look for the desired hash.

        Don't spawn them if there are too many processes running already.

        """
        ranges = get_ranges(300000)
        while True:
            if len(active_children()) < max_processes:
                _min, _max = ranges.next()
                proc = Process(
                    target=queue_if_range_has_enough_leading_zeroes,
                    args=(num_zeroes, _min, _max, result_queue),
                    name='Hasher {_min} - {_max}'.format(_min=_min, _max=_max),
                )
                proc.daemon = True
                proc.start()
            else:
                sleep(.01)

    spawner = Process(target=_process_spawner, name='Spawner')
    spawner.start()
    return spawner


def get_ranges(range_width):
    """Generator that returns sequential ranges with specified width.

    Example:
    Given `range_width` of 10, the generator will yield:
    0, 10
    10, 20
    20, 30
    ...

    """
    i = 0
    while True:
        yield i, i + range_width
        i += range_width


def queue_if_range_has_enough_leading_zeroes(
        num_zeroes, _min, _max, result_queue):
    """Add result to queue if a hash in the range starts with enough 0s.

    Add the amount of zeroes, the number, and the hash to the `result_queue`.

    """
    for i in xrange(_min, _max):
        hsh = sha512(str(i)).hexdigest()
        if hsh.startswith('0' * num_zeroes):
            result_queue.put((num_zeroes, i, hsh))
    # print(_min, 'done')


if __name__ == '__main__':
    main()
