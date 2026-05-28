class SpawnManager:
    def __init__(self, animals_pool, world):
        self.pool = animals_pool
        self.world = world

    def create_animals(self, anim_pool, chunk_clmn, chunk_row, animal, width, height, frames, max_spawn):
        positions = self.world.get_spawn_position(chunk_clmn, chunk_row, max_spawn)
        for world_x, world_y in positions:
            anim = self.pool(anim_pool, animal, world_x, world_y, width, height, frames)
            if anim:
                anim.chunk = (chunk_clmn, chunk_row)
