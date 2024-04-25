import asyncio


async def print_square(num):
    print("Square: {}".format(num * num))


async def print_cube(num):
    print("Cube: {}".format(num * num * num))


async def main():
    # Schedule coroutines to run concurrently
    await asyncio.gather(
        print_square(10),
        print_cube(10)
    )


asyncio.run(main())
