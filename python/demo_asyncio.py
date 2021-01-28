import logging
import asyncio


async def say_after(after, what):
    logging.debug('say_after() start')

    await asyncio.sleep(after)
    logging.info(what)

    logging.debug('say_after() end')


async def set_after(future, after, what):
    logging.debug(f'set_after() start {what}')

    await asyncio.sleep(after)
    future.set_result(what)

    logging.debug('set_after() end')


async def fn():
    logging.debug('fn() start')

    coro1 = say_after(1, 'hello')
    coro2 = say_after(2, 'world')

    task1 = asyncio.create_task(coro1)
    task2 = asyncio.create_task(coro2)

    await task1
    await task2

    logging.debug('fn() tasks done')

    loop = asyncio.get_running_loop()
    future1 = loop.create_future()
    future2 = loop.create_future()

    logging.info("Hello ...")
    loop.create_task(set_after(future1, 3, '... the'))
    loop.create_task(set_after(future2, 3, '... world'))

    logging.debug('Starting future awaiting')

    result1 = await future1
    result2 = await future2

    logging.info(f'Future1 resolved: {result1}')
    logging.info(f'Future2 resolved: {result2}')

    logging.debug('fn() end')


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(thread)6d - %(threadName)s - %(filename)20s - %(lineno)3d - %(levelname)5s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logging.debug('main() start')

    asyncio.run(fn(), debug=True)

    logging.debug('main() end')


if __name__ == '__main__':
    main()
