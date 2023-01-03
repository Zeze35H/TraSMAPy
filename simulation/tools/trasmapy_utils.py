from typing import List, Literal, Optional, TypedDict

from trasmapy import TraSMAPy
from trasmapy.color.Color import Color
from trasmapy.network._Edge import Edge
from trasmapy.network._LaneStop import Stop
from trasmapy.users.VehicleClass import VehicleClass
from trasmapy.users._Route import Route
from trasmapy.users._VehicleType import VehicleType


class Trip(TypedDict):
    id: str
    route: Route
    type: str
    park_areas: List[Stop]
    weight: float

def create_trip(context: TraSMAPy, route_id: str, edges: List[Edge], route_type: Literal["normal", "parking"] = "normal", weight: Optional[float] = None, parks: List[Stop] = []) -> Trip:
    """Creates a trip for simulation

    Args:
        context (TraSMAPy): TraSMAPy context.
        route_id (str): Trip identifier.
        edges (List[Edge]): Edges where agent must pass through.
        route_type (Literal[&quot;normal&quot;, &quot;parking&quot;]): Trip type. Defaults to "normal".
        weight (Optional[float], optional): Weight associated with trip for selection process. Defaults to None.
        parks (List[Stop], optional): Parking areas available for parking when trip type is "parking". Defaults to [].

    Returns:
        Trip: Created trip.
    """
    return Trip(
        id=route_id,
        route=context.users.createRouteFromEdges(routeId=route_id, edges=edges),
        type=route_type,
        weight=weight if weight != None else 1,
        park_areas=parks
    )

def get_default_vtype(context: TraSMAPy, colour: Color = Color(200, 200, 200)) -> VehicleType:
    default_vtype = context.users.getVehicleType("DEFAULT_VEHTYPE")
    default_vtype.color = colour
    return default_vtype

def get_electric_vtype(context: TraSMAPy, colour: Color = Color(50, 50, 255)) -> VehicleType:
    electric_vtype = context.users.getVehicleType("DEFAULT_VEHTYPE").duplicate("evehicle")
    electric_vtype.vehicleClass = VehicleClass.EVEHICLE
    electric_vtype.color = colour
    electric_vtype.emissionClass = "Energy"
    return electric_vtype

def get_bus_vtype(context: TraSMAPy, colour: Color = Color(255, 255, 0)) -> VehicleType:
    bus_vtype = context.users.getVehicleType("DEFAULT_VEHTYPE").duplicate("bus")
    bus_vtype.vehicleClass = VehicleClass.BUS
    bus_vtype.color = colour
    bus_vtype.shape = "bus"
    return bus_vtype

# def assign_routes(context: TraSMAPy, routes:)