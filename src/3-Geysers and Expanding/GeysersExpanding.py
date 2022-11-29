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
ASSIMILATOR = UnitTypeId.ASSIMILATOR


class MSGABot(BotAI):
    async def on_step(self, iteration):
        # what to do every step
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.expand()
        await self.build_assimilator()

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

    async def expand(self):
        if self.townhalls(NEXUS).amount < 2 and self.can_afford(NEXUS):
            await self.expand_now()

    async def build_assimilator(self):
        for nexus in self.townhalls(NEXUS).ready:
            vespenes = self.vespene_geyser.closer_than(15.0, nexus)
            for vespene in vespenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                else:
                    worker = self.select_build_worker(vespene.position)
                    if worker is None:
                        break
                    else:
                        if not self.structures(ASSIMILATOR).closer_than(1.0, vespene).exists:
                            worker.build(ASSIMILATOR, vespene)


def main():
    run_game(maps.get("AbyssalReefLE"), [
        Bot(Race.Protoss, MSGABot()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True)


if __name__ == "__main__":
    main()
