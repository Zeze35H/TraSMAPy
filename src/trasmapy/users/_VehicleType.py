from typing_extensions import override
import traci

from trasmapy._IdentifiedObject import IdentifiedObject
from trasmapy.color._Colorable import Colorable, Color
from trasmapy.users.VehicleClass import VehicleClass

class VehicleType(IdentifiedObject, Colorable):
    def __init__(self, typeId: str) -> None:
        super().__init__(typeId)

    def duplicate(self, cloneId: str):
        if cloneId in traci.vehicletype.getIDList():
            raise ValueError(
                f"There's already a vehicle type with the given ID: [TypeId={cloneId}]"
            )

        traci.vehicletype.copy(self.id, cloneId)
        return VehicleType(cloneId)

    @property
    def length(self) -> float:
        """Returns the length of the vehicles of this type (m)."""
        return traci.vehicletype.getLength(self.id)  # type: ignore

    @length.setter
    def length(self, newVal: float) -> None:
        """Sets the length of the vehicles of this type (m)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError("Length needs to be a number (int/float data type).")
        traci.vehicletype.setLength(self.id, newVal)

    @property
    def maxSpeed(self) -> float:
        """Returns the maximum speed of the vehicles of this type (m/s)."""
        return traci.vehicletype.getMaxSpeed(self.id)  # type: ignore

    @maxSpeed.setter
    def maxSpeed(self, newVal: float) -> None:
        """Sets the maximum speed of the vehicles of this type (m/s)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError("MaxSpeed needs to be a number (int/float data type).")
        traci.vehicletype.setMaxSpeed(self.id, newVal)

    @property
    def maxLateralSpeed(self) -> float:
        """Returns the maximum lateral speed of the vehicles of this type (m/s)."""
        return traci.vehicletype.getMaxSpeedLat(self.id)  # type: ignore

    @maxLateralSpeed.setter
    def maxLateralSpeed(self, newVal: float) -> None:
        """Sets the maximum lateral speed of the vehicles of this type (m/s)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError(
                "MaxLateralSpeed needs to be a number (int/float data type)."
            )
        traci.vehicletype.setMaxSpeedLat(self.id, newVal)

    @property
    def maxAcceleration(self) -> float:
        """Returns the maximum acceleration of the vehicles of this type (m/s^2)."""
        return traci.vehicletype.getAccel(self.id)  # type: ignore

    @maxAcceleration.setter
    def maxAcceleration(self, newVal: float) -> None:
        """Sets the maximum acceleration of the vehicles of this type (m/s^2)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError(
                "MaxAcceleration needs to be a number (int/float data type)."
            )
        traci.vehicletype.setAccel(self.id, newVal)

    @property
    def maxDeceleration(self) -> float:
        """Returns the maximum deceleration of the vehicles of this type (m/s^2)."""
        return traci.vehicletype.getDecel(self.id)  # type: ignore

    @maxDeceleration.setter
    def maxDeceleration(self, newVal: float) -> None:
        """Sets the maximum deceleration of the vehicles of this type (m/s^2)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError(
                "MaxDeceleration needs to be a number (int/float data type)."
            )
        traci.vehicletype.setDecel(self.id, newVal)

    @property
    def vehicleClass(self) -> VehicleClass:
        return VehicleClass(traci.vehicletype.getVehicleClass(self.id))

    @vehicleClass.setter
    def vehicleClass(self, newVal: VehicleClass) -> None:
        if not isinstance(newVal, VehicleClass):
            raise ValueError("MaxDeceleration needs to be an instance of VehicleClass.")
        traci.vehicletype.setVehicleClass(self.id, newVal.value)

    @property
    def emissionClass(self) -> str:
        return traci.vehicletype.getEmissionClass(self.id)  # type: ignore

    @emissionClass.setter
    def emissionClass(self, newVal: str) -> None:
        if not isinstance(newVal, str):
            raise ValueError("EmissionClass needs to be a string.")
        traci.vehicletype.setEmissionClass(self.id, newVal)

    @property
    def shape(self) -> str:
        return traci.vehicletype.getShapeClass(self.id)  # type: ignore

    @shape.setter
    def shape(self, newVal: str) -> None:
        if not isinstance(newVal, str):
            raise ValueError("Shape needs to be a string.")
        traci.vehicletype.setShapeClass(self.id, newVal)

    @property
    def minGap(self) -> float:
        """Returns the offset (gap to front vehicle if halting) of vehicles of this type (m)."""
        return traci.vehicletype.getMinGap(self.id)  # type: ignore

    @minGap.setter
    def minGap(self, newVal: float) -> None:
        """Sets the offset (gap to front vehicle if halting) of vehicles of this type (m)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError("MinGap needs to be a number (int/float data type).")
        traci.vehicletype.setMinGap(self.id, newVal)

    @property
    def minLateralGap(self) -> float:
        """Returns the desired lateral gap of vehicles of this type at 50 km/h (m)."""
        return traci.vehicletype.getMinGapLat(self.id)  # type: ignore

    @minLateralGap.setter
    def minLateralGap(self, newVal: float) -> None:
        """Sets the desired lateral gap of vehicles of this type at 50 km/h (m)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError(
                "MinLateralGap needs to be a number (int/float data type)."
            )
        traci.vehicletype.setMinGapLat(self.id, newVal)

    @property
    def width(self) -> float:
        """Returns the width of vehicles of this type (m)."""
        return traci.vehicletype.getWidth(self.id)  # type: ignore

    @width.setter
    def width(self, newVal: float) -> None:
        """Sets the width of vehicles of this type (m)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError("Width needs to be a number (int/float data type).")
        traci.vehicletype.setWidth(self.id, newVal)

    @property
    def height(self) -> float:
        """Returns the height of vehicles of this type (m)."""
        return traci.vehicletype.getHeight(self.id)  # type: ignore

    @height.setter
    def height(self, newVal: float) -> None:
        """Sets the height of vehicles of this type (m)."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError("Height needs to be a number (int/float data type).")
        traci.vehicletype.setHeight(self.id, newVal)

    @property
    def personCapacity(self) -> float:
        """Returns the total number of people that can ride in a vehicle of this type at the same time."""
        return traci.vehicletype.getPersonCapacity(self.id)  # type: ignore

    @personCapacity.setter
    def personCapacity(self, newVal: int) -> None:
        """Sets the total number of people that can ride in a vehicle of this type at the same time."""
        if not isinstance(newVal, int):
            raise ValueError("PersonCapacity needs to be an int.")
        traci.vehicletype.setPersonCapacity(self.id, newVal)  # type: ignore

    @property
    def scale(self) -> float:
        """Returns the traffic scaling factor of vehicles of this type."""
        return traci.vehicletype.getScale(self.id)  # type: ignore

    @scale.setter
    def scale(self, newVal: float) -> None:
        """Sets the traffic scaling factor of vehicles of this type."""
        if not (isinstance(newVal, float) or isinstance(newVal, int)):
            raise ValueError("Scale needs to be a number (int/float data type).")
        traci.vehicletype.setScale(self.id, newVal)

    @property
    @override
    def color(self) -> Color:
        return Color(*traci.vehicletype.getColor(self.id))

    @color.setter
    @override
    def color(self, color: Color) -> None:
        traci.vehicletype.setColor(self.id, color.colorTupleA)
