import sc2
from sc2 import maps
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

NEXUS = UnitTypeId.NEXUS
PROBE = UnitTypeId.PROBE
PYLON = UnitTypeId.PYLON



class MSGABot(BotAI):
    async def on_step(self, iteration):
        # what to do every step
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()

    async def build_workers(self):
    # nexus = command center
        for nexus in self.townhalls(NEXUS).ready.idle:
            if self.can_afford(PROBE):
                nexus.train(PROBE)

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.townhalls(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=nexuses.first)


def main():
    run_game(maps.get("AbyssalReefLE"), [
        Bot(Race.Protoss, MSGABot()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True)


if __name__ == "__main__":
    main()
