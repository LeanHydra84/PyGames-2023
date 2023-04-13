from pygame import Vector2

splits = 32
reachedThreshold = 10**2 # Distance before target position is considered "reached"

def can_see_point(myPos: Vector2, point: Vector2, state) -> bool:
    direction = (point - myPos).normalize() * (point.distance_to(myPos) / splits)
    adjp = myPos + state.camera
    for i in range(splits - 1):
        if not state.map.get_collision_at_point(adjp + i * direction):
            return False
    return True

def position_reached(myPos: Vector2, pos: Vector2):
    return myPos.distance_squared_to(pos) < reachedThreshold


def move_towards(self, target, speed):
    mov = (target - self.position).normalize()
    self.position += mov * speed
    self.rotation = -(target - self.position).as_polar()[1]