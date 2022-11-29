import sc2
from sc2 import maps
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer
from sc2.bot_ai import BotAI


class MSGABot(BotAI):
    async def on_step(self, iteration):
        # what to do every step
        await self.distribute_workers()


def main():
    run_game(maps.get("AbyssalReefLE"), [
        Bot(Race.Protoss, MSGABot()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True)


if __name__ == "__main__":
    main()
