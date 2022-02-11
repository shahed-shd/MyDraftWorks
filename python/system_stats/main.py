import time
import logging
import log
import psutil
import sys
from typing import Final


INTERVAL_IN_SEC = 1
NETWORK_DATA_UNIT = 'KiB'
NETWORK_DATA_UNIT_DENOMINATOR = 1024

logger: logging.Logger = log.logger


def read_network_io_total(network_interface: str = None) -> tuple[int, int]:
    try:
        counter: psutil.snetio = psutil.net_io_counters(pernic=True)[network_interface] if network_interface else psutil.net_io_counters()
        return counter.bytes_sent, counter.bytes_recv
    except KeyError:
        logger.error(f'Network interface {network_interface} not found')

    return 0, 0


def main():
    # CLI args
    network_interface: Final[str] = sys.argv[1] if len(sys.argv) > 1 else None

    # Debug messages
    logger.debug(f'Selected network interface: {network_interface}')
    logger.debug(f'Interval in secs: {INTERVAL_IN_SEC}')
    logger.debug(f'Network IO speed unit: {NETWORK_DATA_UNIT}/sec')

    prev_t = time.time()
    prev_net_io_total: tuple[int, int] = read_network_io_total(network_interface=network_interface)

    while(True):
        try:
            time.sleep(INTERVAL_IN_SEC)

            curr_t = time.time()
            curr_net_io_total: tuple[int, int] = read_network_io_total(network_interface=network_interface)

            cpu = psutil.cpu_percent()
            vmem = psutil.virtual_memory().percent
            swp = psutil.swap_memory().percent
            sent_rate, recv_rate = [(curr_tot - prev_tot) / (curr_t - prev_t) / NETWORK_DATA_UNIT_DENOMINATOR
                                    for curr_tot, prev_tot in zip(curr_net_io_total, prev_net_io_total)]

            msg: str = (
                f'cpu: {cpu:7.3f}'
                f'\tvmem: {vmem:7.3f}'
                f'\tswp: {swp:7.3f}'
                f'\tTx: {sent_rate:10.3f}'
                f'\tRx: {recv_rate:10.3f}'
            )

            prev_t = curr_t
            prev_net_io_total = curr_net_io_total

            logger.info(msg)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
