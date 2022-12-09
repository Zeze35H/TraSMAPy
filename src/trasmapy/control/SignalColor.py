from enum import Enum


class SignalColor(Enum):
    RED_LIGHT = "r"
    """red light - vehicles must stop"""

    YELLOW_LIGHT = "y"
    """yellow light - vehicles start to decelerate if far away, otherwise they shall pass"""

    GREEEN_LIGHT_NO_PRIORITY = "g"
    """green light, no priority - vehicle may pass the junction if there is not a vehicle using a higher priorised stream, otherwise they let it pass.
        They always decelerate on approach until they are within the configured visibility distance"""

    GREEEN_LIGHT_PRIORITY = "G"
    """green light, priority - vehicle may pass the junction"""

    GREEN_RIGHT_TURN = "s"
    """green right-turn arrow requires stopping - vehicles may pass the junction if no vehicle uses a higher priorised foe stream. They always stop before passing. This is only generated for junction type traffic_light_right_on_red."""

    ORANGE_LIGHT = "u"
    """red + yellow light - indicates upcoming green light. However, vehicles may not pass yet."""

    BROWN_LIGHT = "o"
    """off, blinking - signal is switched off, blinking indicates that vehicles have to yield"""

    BLUE_LIGHT = "O"
    """off, no signal - signal is switched off, vehicles have the right of way"""
