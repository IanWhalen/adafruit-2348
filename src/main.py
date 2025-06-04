import asyncio
from viam.module.module import Module
from models.adafruit_2348 import Adafruit2348

if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
