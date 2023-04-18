import pygame
import json
import random

from map.spawner import spawn

rooms = []
hallways = []

SCALE = 5

def readalltext(fpath):
    file = open(fpath)
    text = file.read()
    file.close()
    return text

class HallwayArchetype:
    def __init__(self, obj):
        self.name = obj['name']
        
        self.image = pygame.transform.scale_by(pygame.image.load(obj['path']).convert_alpha(), SCALE)
        self.collider = pygame.transform.scale_by(pygame.image.load(obj['collider']).convert_alpha(), SCALE)
        self.exits = obj['exits']
        self.spawns = obj['spawns']


class HallwayActual(pygame.sprite.Sprite):
    def __init__(self, image, collider, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.collider = collider

        self.position = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=pos)
        self.is_dead_end = False

    def update(self, state):
        self.rect.center = self.position + state.camera

class RoomArchetype(pygame.sprite.Sprite):
    def __init__(self, obj):
        self.image = pygame.transform.scale_by(pygame.image.load(obj['path']).convert_alpha(), SCALE)
        self.collider = pygame.transform.scale_by(pygame.image.load(obj['collider']).convert_alpha(), SCALE)

        self.doorPos = [p * SCALE for p in obj['doorpos']]
        self.doorForward = obj['doorforward']
        self.spawns = obj['spawns']

class ROOMLOADER:
    def __init__(self):
        decoder = json.decoder.JSONDecoder()
        
        hwJSON = readalltext("assets\\R2\\hallways.json")
        hallwaysobject = decoder.decode(hwJSON)
        self.hallways = [HallwayArchetype(p) for p in hallwaysobject if "disabled" not in p]

        deadend = readalltext("assets\\R2\\deadend.json")
        deadendobj = decoder.decode(deadend)
        self.deadend = HallwayArchetype(deadendobj)

        roomsjson = readalltext("assets\\R2\\rooms.json")
        roomsobj = decoder.decode(roomsjson)
        self.rooms = [RoomArchetype(p) for p in roomsobj]
        

    def find_hallway(self, name) -> HallwayArchetype:
        return [p for p in self.hallways if p.name == name][0]
    
    def get_hallway(self) -> HallwayArchetype:
        return random.choice(self.hallways)
    
    def get_room(self):
        pass

    def find_room(self, name):
        return [p for p in self.rooms if p.name == name][0]
    
    def get_end_cap(self):
        return self.deadend

class BuildDetails:
    def __init__(self, group):
        self.uncappedEnds = 0
        self.deadEnds = []
        self.spawns = []
        self.group = group
        self.spawnIndex = 1

        self.hm_spawnquota = 15
        self.tch_spawnquota = 5

def rotate_90(coord: list):
    # Clockwise rotation: [x, y] ==> [y, -x]
    temp = coord[0]
    coord[0] = coord[1]
    coord[1] = -temp


def tuple_multiply(t1, t2):
    return tuple(t1[i] * t2[i] for i in range(len(t1)))

def tuple_sum(t1, t2):
    return tuple(t1[i] + t2[i] for i in range(len(t1)))

def multipy_tuple_then_sum(t1, t2):
    return sum(tuple_multiply(t1, t2))

def rotate_until_equal(p1, p2) -> int:
    orientationCounter = 0
    while orientationCounter < 4:
        if p1 == p2:
            break
        else:
            orientationCounter += 1
            rotate_90(p1)
    return orientationCounter

# SOOOOOO MUCH DUPLICATE AND DISGUSTING CODE HERE!!!!!!! I NEED TO FIX THAT!!!

def place_dead_end(map, resource, pos, direction):
    nextr = resource.get_end_cap()

    chosenExit = nextr.exits[0].copy()
    revDirection = [-direction[0], -direction[1]]

    orientationCounter = rotate_until_equal(chosenExit, revDirection)

    IMAGE = pygame.transform.rotate(nextr.image, orientationCounter * 90)
    COLLIDER = pygame.transform.rotate(nextr.collider, orientationCounter * 90)

    scalar = abs(multipy_tuple_then_sum(IMAGE.get_rect().size, direction))
    posDelta = pygame.Vector2(direction) * scalar * 0.5
    hw = HallwayActual(IMAGE, COLLIDER, posDelta + pos)
    hw.is_dead_end = True

    # This little block detects overlapping dead end pieces and removes them to make a continuous hallway    
    collided = pygame.sprite.spritecollide(hw, map.group, False, pygame.sprite.collide_rect_ratio(1.1))
    for other in collided:
        if other.is_dead_end and ((other.position.x == hw.position.x) or (other.position.y == hw.position.y)):
            #print("Deleting double. You're welcome, map geometry.")
            other.kill()
            return
    

    map.group.add(hw)


def _recurse_generate_hallways(details: BuildDetails, resource, pos, direction, depth, lastroom, forceroom = None):
    if depth <= 0:
        details.deadEnds.append( (pos, direction) )
        return

    nextr: HallwayArchetype = resource.get_hallway()
    if nextr == lastroom:
        nextr = resource.get_hallway() # Retakes, as to lower the chances of getting two in a row

    _exits = [p.copy() for p in nextr.exits]
    chosenexit = random.choice(_exits)
    _exits.remove(chosenexit)

    # Yes, I know this is duplicate code that will run almost the same thing twice and replace its results.
    # This is fine because forceroom should only ever be nonnull once. Also this is due tomorrow so we're getting janky
    if forceroom != None:
        # forceroom is super janky. it's a tuple with [0] = a roomarchetype and [1] = the index of the exit to use
        nextr = forceroom[0]
        _exits = [p.copy() for p in nextr.exits]
        chosenexit = _exits[forceroom[1]]
        _exits.remove(chosenexit)
        

    revDirection = [-direction[0], -direction[1]]

    # Rotate Room To Correct Orientation ==> [chosenexit == revDirection]

    orientationCounter = rotate_until_equal(chosenexit, revDirection)


    IMAGE = pygame.transform.rotate(nextr.image, orientationCounter * 90)
    COLLIDER = pygame.transform.rotate(nextr.collider, orientationCounter * 90)

    # ALIGN NEW ROOM (x, y) ENTRANCE WITH CURRENT EXIT

    scalar = abs(multipy_tuple_then_sum(IMAGE.get_rect().size, direction))
    posDelta = pygame.Vector2(direction) * scalar * 0.5

    hw = HallwayActual(IMAGE, COLLIDER, posDelta + pos)

    if len(pygame.sprite.spritecollide(hw, details.group, False)) > 0:
        place_dead_end(details, resource, pos, direction)
        return

    details.group.add(hw)
    add_spawns(nextr.spawns, pygame.Vector2(hw.rect.center), details.spawns, orientationCounter)

    # Rotate each exit from _exits to match orientation,
    for d in _exits:
        for i in range(orientationCounter):
            rotate_90(d)

        add = tuple_multiply(hw.rect.size, d)
        add = tuple(p * 0.5 for p in add)
        newPos = tuple_sum(hw.rect.center, add)

        #pygame.draw.circle(main.DEBUGSCREEN, pygame.Color(255, 0, 0), newPos, 25)
        
        details.uncappedEnds += 1
        _recurse_generate_hallways(details, resource, newPos, d, depth - 1, nextr)

def add_spawns(spawns, localCenter, spawnlist: list, orientation):
    for s in spawns:
        rotatedoffset = [p * SCALE for p in s['position']]

        for i in range(orientation):
            rotate_90(rotatedoffset)

        adjustpos = localCenter + rotatedoffset
        chance = s['chance']

        spawnlist.append([s['type'], adjustpos, chance])

def try_place_room(group, pos, direction, archetype: RoomArchetype, details):
    revDirection = [-direction[0], -direction[1]]
    
    forward = archetype.doorForward.copy()
    orientation = rotate_until_equal(forward, revDirection)

    IMAGE = pygame.transform.rotate(archetype.image, orientation * 90)
    COLLIDER = pygame.transform.rotate(archetype.collider, orientation * 90)

    localdoorpos = archetype.doorPos.copy()
    for _ in range(orientation):
        rotate_90(localdoorpos)

    localizedCenter = pygame.Vector2(pos) - pygame.Vector2(localdoorpos)

    newroom = HallwayActual(IMAGE, COLLIDER, localizedCenter)
    if pygame.sprite.spritecollide(newroom, group, False):
        return False
    else:
        group.add(newroom)
        add_spawns(archetype.spawns, localizedCenter, details.spawns, orientation)
        return True

def _tuple_sort_by_distance(sp):
    tup = sp[1]
    return tup[0]*tup[0] + tup[1]*tup[1]

class Mapv2:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.details = BuildDetails(self.group)

    def get_collision_at_point(self, point) -> bool: # True means valid position, false means collision
        for x in self.group:
            if x.rect.collidepoint(point):
                col: pygame.Surface = x.collider
                color = col.get_at( (int(point.x - x.rect.x), int(point.y - x.rect.y)) )
                if color.r == 255:
                    return True
                #return False # Commenting this could lead to more lag?
        return False

    def get_inside(self, sprite : pygame.sprite.Sprite):
        collist = pygame.sprite.spritecollide(sprite, self.group, False)
        if len(collist) > 0:
            return collist
        return None

    def spawn_all(self, state, onlyEnemies = False):
        sortedspawns = sorted(self.details.spawns, key=_tuple_sort_by_distance)

        hmcount = self.details.hm_spawnquota

        #trcount = self.details.tch_spawnquota if self.details.spawnIndex > 1 else self.details.tch_spawnquota // 2

        # Guarantee spawns for first N monitors and teachers, by distance from spawn
        for s in sortedspawns:
            if s[0] == "HallMonitor" and hmcount > 0:
                s[2] = 1
                hmcount -= 1

        for s in sortedspawns:
            type = s[0]

            if onlyEnemies and not (type == "HallMonitor" or type == "Teacher" or type == "Either"):
                continue

            if self.details.spawnIndex == 0:
                if s[0] == "Teacher":
                    continue
                if s[0] == "Either":
                    type = "HallMonitor"


            if random.random() < s[2]:
                spawn(type, s[1], state)

def createmap(depth):
    attempts = 0

    while True:
        resource = ROOMLOADER()

        nmap = Mapv2()

        setflag = True
        startcoord = (0, -15 * SCALE)

        try_place_room(nmap.group, startcoord, (0, 1), resource.rooms.pop(0), nmap.details)
        hallwaybase = resource.hallways.pop(0)

        _recurse_generate_hallways(nmap.details, resource, startcoord, (0, -1), depth + 1, None, (hallwaybase, 0))

        if nmap.details.uncappedEnds < len(resource.rooms):
            attempts += 1
            continue
        
        roomcopy = resource.rooms.copy()
        randomizedDeadends = random.sample(nmap.details.deadEnds, len(nmap.details.deadEnds))

        while len(roomcopy) > 0:
            room = random.choice(roomcopy)
            roomcopy.remove(room)

            setflag = False
            for end in nmap.details.deadEnds:
                success = try_place_room(nmap.group, end[0], end[1], room, nmap.details)
                if success:
                    randomizedDeadends.remove(end)
                    setflag = True
                    break

            if not setflag:
                break

        for end in randomizedDeadends:
            place_dead_end(nmap, resource, end[0], end[1])

        if not setflag:
            attempts += 1
            continue
        else:
            return nmap

