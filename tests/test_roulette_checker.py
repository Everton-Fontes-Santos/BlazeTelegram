from blazetelegrambot.services.roulette_checker import RouletteChecker
from blazetelegrambot.infrastructure.httpx_client import HTTPXClient


async def test_roulette_checker():
    http = HTTPXClient()
    service = RouletteChecker(web_client=http)
    doubles = await service.execute({})
    assert doubles != None