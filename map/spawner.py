from character.teacher import Teacher
from character.hallmonitor import HallMonitor
from character.pickup import Pickup
from character.mrsflips import MrsFlips

import random as rand

def init_hallmonitor_atpos(state, pos):
    en = HallMonitor(state.RESOURCES.HALLMONITOR, state.RESOURCES.FEET, state)
    en.position = pos
    en.rotation = rand.randrange(0, 360)

    state.renderLayers.add_to("Enemies", en)
    state.renderLayers.add_to("Feet", en.feet)

def init_teacher_atpos(state, pos):
    en = Teacher(state.RESOURCES.TEACHER, state.RESOURCES.FEET, state)
    en.position = pos
    en.rotation = rand.randrange(0, 360)

    state.renderLayers.add_to("Enemies", en)
    state.renderLayers.add_to("Feet", en.feet)

def spawn(type: str, pos, state):
    if type == "MrsFlips":
        char = MrsFlips(state.RESOURCES.MRS_FLIPS, pos)
        state.renderLayers.add_to("Interactable", char)
    elif type == "HallMonitor":
        init_hallmonitor_atpos(state, pos)
    elif type == "Teacher":
        init_teacher_atpos(state, pos)
    else:
        pass # Pickups using type == pickupname????