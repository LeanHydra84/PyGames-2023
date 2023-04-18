from character.teacher import Teacher
from character.hallmonitor import HallMonitor
from character.pickup import Pickup
from character.mrflip import MrFlip
from character.computer import Computer

import random as rand

def init_hallmonitor_atpos(state, pos):
    en = HallMonitor(state.RESOURCES.HALLMONITOR, state.RESOURCES.FEET, state)
    en.position = pos
    en.rotation = rand.randrange(0, 360)

    state.renderLayers.add_to("Enemies", en)
    state.renderLayers.add_to("Feet", en.feet)

    en.update(state)


def init_teacher_atpos(state, pos):
    en = Teacher(state.RESOURCES.TEACHER, state.RESOURCES.FEET, state)
    en.position = pos
    en.rotation = rand.randrange(0, 360)

    state.renderLayers.add_to("Enemies", en)
    state.renderLayers.add_to("Feet", en.feet)

    en.update(state)

def spawn(type: str, pos, state):

    if type == "Either":
        type = rand.choice(["HallMonitor", "Teacher"])

    if type == "MrsFlips":
        char = MrFlip(state.RESOURCES.MRS_FLIPS, pos)
        state.renderLayers.add_to("Interactable", char)
    elif type == "HallMonitor":
        init_hallmonitor_atpos(state, pos)
    elif type == "Teacher":
        init_teacher_atpos(state, pos)

    elif type == "Ruler":
        ruler = Pickup(state.RESOURCES.RULER, "Ruler", pos, state.RESOURCES.RULER_HINT)
        state.renderLayers.add_to("Interactable", ruler)

    elif type == "Tray":
        tray = Pickup(state.RESOURCES.TRAY, "Tray", pos, state.RESOURCES.TRAY_HINT)
        state.renderLayers.add_to("Interactable", tray)

    elif type[:5] == "CMPTR":
        branch = type[5:]
        computer = Computer(state.RESOURCES.COMPUTER, state.RESOURCES.COMPUTER_OFF, pos, branch)
        state.renderLayers.add_to("Interactable", computer)

    return type